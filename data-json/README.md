# JSON API

The JSON files in this dataset can be used as an API. 

## JSON API structure

Example provincial JSON API. 

```
{
  "schema": {
    "fields": [
      {
        "name": "Datum",
        "type": "string"
      },
      {
        "name": "Provincienaam",
        "type": "string"
      },
      {
        "name": "Provinciecode",
        "type": "integer"
      },
      {
        "name": "overledenAantal",
        "type": "integer"
      },
      {
        "name": "totaalAantal",
        "type": "integer"
      },
      {
        "name": "ziekenhuisopnameAantal",
        "type": "integer"
      },
      {
        "name": "overledenAantalCumulatief",
        "type": "integer"
      },
      {
        "name": "totaalAantalCumulatief",
        "type": "integer"
      },
      {
        "name": "ziekenhuisopnameAantalCumulatief",
        "type": "integer"
      }
    ]
  },
  "data": [
    {
      "Datum": "2020-05-24",
      "Provincienaam": "Drenthe",
      "Provinciecode": 22,
      "overledenAantal": 0,
      "totaalAantal": 0,
      "ziekenhuisopnameAantal": 0,
      "overledenAantalCumulatief": 40,
      "totaalAantalCumulatief": 506,
      "ziekenhuisopnameAantalCumulatief": 116
    },
  
    ...
  
    {
      "Datum": "2020-05-24",
      "Provincienaam": "Zuid-Holland",
      "Provinciecode": 28,
      "overledenAantal": 3,
      "totaalAantal": 45,
      "ziekenhuisopnameAantal": 3,
      "overledenAantalCumulatief": 1187,
      "totaalAantalCumulatief": 9686,
      "ziekenhuisopnameAantalCumulatief": 2103
    }
  ],
  "apiVersion": "0.1"
}
```
