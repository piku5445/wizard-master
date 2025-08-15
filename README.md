# All UDP Code Body

## Get the status of a light or plug
```json
{"method":"getPilot","params":{}}
```

## Set my light to a custom RGB color
```json
{"method":"setPilot","params":{"r":255,"g":0,"b":0}}
```

## Turn a Light or Plug OFF/ON
```json
{"method":"setState","params":{"state":false}}
```

## Set Brightness
- Choose a value between 10-100. (10 represents the lowest possible brightness)
```json
{"method":"setState","params":{"dimming":100}}
```

## Set my light to a scene from the default WiZ app
- For Speed, choose a value between 10-200.
```json
{"method":"setPilot","params":{"sceneId":0,"speed":123}}
```

## Set my light to a custom warm/cool white Temp in Kelvin
- Values: 2200/6200
```json
{"method":"setPilot","params":{"temp":2200}}
```
Update notes for 11 Aug
Minor refactor
Minor refactor
