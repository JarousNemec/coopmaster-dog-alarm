# coopmaster-dog-alarm
- aplikace vyhodnocujici pritomnost nepratel hrabaveho ptactva (psa)

## funkcionalita
- aplikace v pravidelnych intervale vyhodnocuje prehledovy zaber z ohrady
- v aktualniho snimku detekuje pritomnost psa 
- pokud je pes detekovan je tato skutecnost predana do MQTT clienta a nasledne notifikovan HomeAssistant
- uklada aktualni snimek ohrady
- v pripade detekce je snimek se psem pridan do extra adresare pripadne do relacni databaze

## technologie
- python
- vypsat knihovny z requirements
- customizovane Yolo11 
- 

## fancy vecicky -  
- vyuka vlastni modelu 
- detekce vicero druhu nepratel 
- segmentace obrazu
- nutnost graficke karty, grafickych akceleratoru Google Coral, 