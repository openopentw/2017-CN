# header formats

## original udp haeder

```
0      7 8     15 16    23 24    31
+--------+--------+--------+--------+
|      Source     |   Destination   |   <-- original header
|       Port      |       Port      |
+--------+--------+--------+--------+
|      Length     |     Checksum    |
+--------+--------+--------+--------+
|              payload              |   <-- add custom header here
|                ...                |
|                ...                |
+--------+--------+--------+--------+
```

after adding the custom header...

```
0      7 8     15 16    23 24    31
+--------+--------+--------+--------+
|      Source     |   Destination   |   <-- original header
|       Port      |       Port      |
+--------+--------+--------+--------+
|      Length     |     Checksum    |
+--------+--------+--------+--------+
|           custom header           |   <-- added custom header
+--------+--------+--------+--------+
|          original payload         |
|                ...                |
|                ...                |
+--------+--------+--------+--------+
```

## custom haeder

- to agent

	```
	0      7 8     15 16    23 24    31
	+--------+--------+--------+--------+
	|        destination address        |
	+--------+--------+--------+--------+
	|   destination   |      packet     |
	|       port      |      index      |
	+--------+--------+--------+--------+
	|ack_type|  zero  |     ack num     |
	+--------+--------+--------+--------+
	```

- to server/receiver

	```
	0      7 8     15 16    23 24    31
	+--------+--------+--------+--------+
	|           source address          |
	+--------+--------+--------+--------+
	|      source     |      packet     |
	|       port      |      index      |
	+--------+--------+--------+--------+
	|ack_type|  zero  |     ack num     |
	+--------+--------+--------+--------+
	```
