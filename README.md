### Team settings
- Min playtime block size [Implementation started]
- Max playtime block size [Implementation started]
- Play once a day [Not yet implemented]
- Excluded days [Not yet implemented]

### Teams json format

```json
{
	"team_name": [fieldportion(0=Whole,1=Half,2=Quarter), 
		          gametime(int), 
				  priority(uint), 
				  fieldtype(0=Natural,1=Synthetic)
				  [min_playtime_block_size, max_playtime_block_size] 
				  ]
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
