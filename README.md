### Team settings
- Min playtime 
- Max playtime
- Play once a day
- Excluded days

### Teams json format

```json
{
	"team_name": [fieldportion(0=Whole,1=Half,2=Quarter), gametime(int), priority(uint), fieldtype(0=Natural,1=Synthetic)]
}
```

### Field json format

```json
{
	"field_name": {
	  "type": 0=Natural, 1=Synthetic,
	  "periods": {
		 "mon": [[start_hour(0-24), duration], [start_hour(0-24), duration]]
		 "tue": []
		 ...
		 }
	}
}
```
