import sys
import json
import uuid
import random
from datetime import datetime
from kafka import KafkaProducer

print(sys.path)
# Configuración del productor Kafka
producer = KafkaProducer(bootstrap_servers='kafka:9094',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def generate_data():
    # Genera datos aleatorios según el formato especificado.

    device_os = ["ANDROID 10", "IOS 13", "WINDOWS 10", "MACOS 11"]
    device_type = ["ANDROID", "IOS", "WINDOWS", "MAC"]
    browser_type = ["CHROME", "FIREFOX", "SAFARI", "EDGE"]
    isp_names = ["TELCEL", "IZZI", "TELMEX", "AXTEL"]

    mexican_cities = [
        {"city": "CIUDAD DE MÉXICO", "region": "CDMX", "latitude": 19.432608, "longitude": -99.133208},
        {"city": "GUADALAJARA", "region": "JALISCO", "latitude": 20.67359, "longitude": -103.343803},
        {"city": "MONTERREY", "region": "NUEVO LEÓN", "latitude": 25.67507, "longitude": -100.318466},
        # ... (puede agregar más ciudades de México si lo desea)
    ]

    chosen_city = random.choice(mexican_cities)

    data = {
        "content": {
            "specversion": "1.0",
            "id": str(uuid.uuid4()),
            "source": "enrichment-api",
            "type": "enrichment.fct.iovation.v1",
            "data": {
                "id": str(uuid.uuid4()),
                "cached": False,
                "result": {
                    "id": str(uuid.uuid4()),
                    "reason": "Risky Countries",
                    "result": "R",
                    "details": {
                        "device": {
                            "os": random.choice(device_os),
                            "type": random.choice(device_type),
                            "alias": random.randint(10**15, 10**16-1),
                            "isNew": False,
                            "screen": f"{random.randint(800,1000)}X{random.randint(400,500)}",
                            "browser": {
                                "type": random.choice(browser_type),
                                "version": f"{random.randint(90,110)}.0.0.0",
                                "language": "ES-MX",
                                "timezone": "360",
                                "cookiesEnabled": True,
                                "configuredLanguage": "ES-MX,ES-419;Q=0.9,ES;Q=0.8"
                            },
                            "firstSeen": datetime.utcnow().isoformat(),
                            "blackboxMetadata": {
                                "age": random.randint(1,10),
                                "timestamp": datetime.utcnow().isoformat()
                            }
                        },
                        "realIp": {
                            "isp": random.choice(isp_names),
                            "source": "iovation",
                            "address": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                            "ipLocation": {
                                "city": chosen_city["city"],
                                "region": chosen_city["region"],
                                "country": "MEXICO",
                                "latitude": chosen_city["latitude"],
                                "longitude": chosen_city["longitude"],
                                "countryCode": "MX"
                            },
                            "parentOrganization": random.choice(isp_names)
                        },
                        # ... (puede continuar de manera similar para el resto de campos)
                    },
                },
                "status": "success"
            },
            "datacontenttype": "application/json"
        },
        "content_type": {
            "string": "application/cloudevents+json; charset=utf-8",
            "media_type": "application",
            "subtype": "cloudevents+json",
            "subtype_base": "cloudevents",
            "subtype_format": "json",
            "params": [["charset","utf-8"]],
            "charset": "utf-8",
            "error_message": None,
            "canonical_string": "application/cloudevents+json; charset=utf-8"
        }
    }

    return data

def send_to_kafka(topic, data):
    producer.send(topic, data)
    producer.flush()

def main():
    topic = "enrichment.fct.iovation.v1"
    data = generate_data()
    send_to_kafka(topic, data)

if __name__ == "__main__":
    main()
