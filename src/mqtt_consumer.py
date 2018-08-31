from .models import *
import json
import logging

def msg_handler(topic, message, mqttClient, redisClient):
    logger = logging.getLogger()
    sp = topic.split("/")
    # Topic structure: /inbox/<orgId>/<devId>/<topic_detail>
    if len(sp) is 5:
        topic_detail = sp[4]
        org_id = sp[2]
        dev_id = sp[3]
        # Creates the response topic format
        response_topic = "/inbox/{0}/{1}/deviceStatus".format(org_id, dev_id)
        response_message = {"status": "NOK"}
        if "newDevice" == topic_detail:
            # Receive new device registration
            # Expects topic like /outbox/{orgId}/{deviceId}/newDevice
            org = Organization.objects(id=org_id).first()
            # Creates the topic to listen to
            listen_topic = "/inbox/{0}/{1}/#".format(org_id, dev_id)

            if org is not None and "auth_token" in message.keys():
                org_token = message["auth_token"]
                # If device is valid, starts listening to it
                if bcrypt.checkpw(org_token, org.auth_token):
                    logger.info("[MQTT] New device successfully accepted!")
                    # Changes reponse message to successfull
                    response_message = {"status": "OK"}
                    # Creates the device in the DB, and adds it to the org
                    new_dev = Device(id=dev_id, name="new Device")
                    try:
                        new_dev.save()
                        org.devices.append(new_dev)
                        org.save()
                    except Exception as e:
                        print(e)
                        logger.error("[MQTT] Exception ocurred while creating new device")
                    # Starts listening to all device information available
                    mqttClient.subscribe(listen_topic)
                else:
                    logger.warning("[MQTT] Device unathorized to send data")
            else:
                logger.warning("[MQTT] Organization not found or missing auth_token")
            # Sends response back to device
            mqttClient.publish(response_topic, json.dumps(response_message))
        elif "deviceInfo" == topic_detail:
            # Received update on device properties
            # Expects topic like /outbox/{orgId}/{deviceId}/deviceInfo
            # This is the first message received after newDevice,
            # and should be received sporadically
            device = None
            if "endPoints" in message.keys():
                endpoints = []
                req_fields = set([k for k,v in Endpoint._fields.items() if v.required])
                for end in message["endPoints"]:
                    # Check if the endpoint contains all the required fields
                    if set(end.keys()).intersection(req_fields) == req_fields:
                        endpoints.append(Endpoint(**end))
                if len(endpoints) > 0:
                    device = Device.objects(id=dev_id).update_one(
                        add_to_set=endpoints,
                        upsert = True
                        )
            if "name" in message.keys():
                device = Device.objects(id=dev_id).update_one(set__name=message["name"])
            if "description" in message.keys():
                device = Device.objects(id=dev_id).update_one(set__description=message["description"])
            if "status" in message.keys():
                # If the status message is valid, updates it
                if len(set(message["status"]).intersection(set(DEVICE_STATUS))) > 0:
                    device = Device.objects(id=dev_id).update_one(set__status=message["status"])
            if device is not None:
                # Sends data to Redis for caching/showing in Dash (Plotly.js)
                redis_key = "{0}:{1}:deviceInfo".format(org_id, dev_id)
                redisClient.set(redis_key, json.dumps(device))
        elif "lwt" == topic_detail:
            # Received last will from device
            # Expects topic like /outbox/{orgId}/{deviceId}/lwt
            # Updates device info
            device = Device.objects(id=dev_id).update_one(set__status=DEVICE_STATUS[-1])
            # Sends data to Redis for caching/showing in Dash (Plotly.js)
            redis_key = "{0}:{1}:deviceInfo".format(org_id, dev_id)
            redisClient.set(redis_key, json.dumps(device))
        else:
            # Assumes that there is new data incoming from the device
            # Expects topic like /outbox/{orgId}/{deviceId}/{endPointName}
            device = Device.objects(id=dev_id, endpoints__name=topic_detail).first()
            if device is not None:
                # Validates coming data with the model stored in the DB
                valid_endpoints = set(device.endpoints[0].values)
                msg_keys = set(message.keys())
                if valid_endpoints.intersection(msg_keys) == msg_keys:
                    # Sends data to Redis for caching/showing in Dash (Plotly.js)
                    redis_topic = "{0}:{1}:{2}".format(org_id, dev_id, topic_detail)
                    redisClient.publish(redis_topic, json.dumps(message))
                else:
                    logger.warning("[MQTT] Discarded message. Invalid/missing fields for endPoint found")
            else:
                logger.warning("[MQTT] Device endpoint not found: %s", topic_detail)
    else:
        # Topic is not as expected
        logger.warning("[MQTT] Unexpected device topic: %s", topic)