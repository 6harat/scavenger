# scavenger:

* overview:

* quickstart:

* todo:
- [ ] add proper types to atleast all public apis
- [ ] use generics as necesssary to improve public apis
- [ ] use exception parser rather than duplicating validation logic in adapter and controller
- [ ] convert all errors in playmate and internal to domain_error
- [ ] configure setup to enable type checking during compilation
- [ ] make static functions cached
- [ ] add proper validations at all places
- [ ] move all sensible imports to __init__.py to clean imports in files
- [ ] make logging async using https://github.com/B2W-BIT/aiologger
- [ ] validate all async for and convert them to asyncio.gather
- [ ] implement power failure mitigation
- [ ] implement wifi connection lost mitigation (by pausing all active requests for some time)
- [ ] after network interruption re-establish client sesssion as the previous session wont work
- [ ] look into the reason of the following error (probably socket timeout):
	```python
	protocol: <asyncio.sslproto.SSLProtocol object at 0x0000011F1B8CB7F0>
	transport: <_SelectorSocketTransport fd=3388 read=polling write=<idle, bufsize=0>>
	Traceback (most recent call last):
	File "c:\users\bharat\anaconda3\Lib\asyncio\sslproto.py", line 526, in data_received
		ssldata, appdata = self._sslpipe.feed_ssldata(data)
	File "c:\users\bharat\anaconda3\Lib\asyncio\sslproto.py", line 207, in feed_ssldata
		self._sslobj.unwrap()
	File "c:\users\bharat\anaconda3\Lib\ssl.py", line 767, in unwrap
		return self._sslobj.shutdown()
	ssl.SSLError: [SSL: KRB5_S_INIT] application data after close notify (_ssl.c:2592)
	```