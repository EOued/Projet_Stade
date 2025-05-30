### Dependancies
- Python 3 (Tested on python 3.13.3)

### Installation
`git clone https://github.com/EOued/Projet_Stade.git`\
`cd Projet_Stade`\
`python fitter.py`


### Team settings
- Min playtime block size [Implemented]
- Max playtime block size [Implemented]
- Play once a day [Not yet implemented]
- Excluded periods [Implemented]

### Teams json format

```json
{
	"team_name": {
		"values": [fieldportion(0=Whole,1=Half,2=Quarter), 
		          gametime(int), 
				  priority(uint), 
				  fieldtype(0=Natural,1=Synthetic)
				  [min_playtime_block_size, max_playtime_block_size] 
				  ],
	    "excluded_days": [int, int, int...] /* Binary mask (24 bits) for each days, 1 means that the hour is excluded. 0 is no day excluded, 16777215 whole day excluded. 128 for example means that 7h-8h is excluded*/
    }	
}
```

### Field json format

```json
{
	"field_name": {
	  "type": 0=Natural, 1=Synthetic,
	  "periods": [int, int, int] 	/* Binary mask (24 bits) for each days, 1 means that the field on specified hour is usable. 0 is no field unplayable for the day. 3840 for example means that field is available from 8 to 12*/}
}
```
