from APIApp import APIApp

import math
import hilbert
import socket, struct

class spacetime (APIApp):

    def __init__(self):
        APIApp.__init__(self, 'xml')

        self.precision = 8
        self.factor = math.pow(10, self.precision)

    def generate_response (self, x, y, z, h):
        return {'spacetime' : { 'x' : x, 'y' : y, 'z' : z, 'id' : h }}

class spacetimeWOE (spacetime):

    def generate_response (self, woeid, ts, h):
        return {'spacetime' : { 'woeid' : woeid, 'timestamp' : ts, 'id' : h }}

class spacetimeIP (spacetime):

    def generate_response (self, addr, ts, h):
        return {'spacetime' : { 'ip' : addr, 'timestamp' : ts, 'id' : h }}

    # http://code.activestate.com/recipes/66517/
    # {{{ Recipe 66517 (r1): IP address conversion functions with the builtin socket module 
    # IP address manipulation functions, dressed up a bit

    def iptoint(self, ip):
        "convert decimal dotted quad string to long integer"
        return struct.unpack('L', socket.inet_aton(ip))[0]

    def intoip(self, n):
        "convert long int to dotted quad string"
        return socket.inet_ntoa(struct.pack('L',n))



class Main(spacetime):

    def get (self):

        self.response.out.write("""

<style type="text/css">

.main{
margin:100px;
font-family:sans-serif;
}

.request{
margin:30px;
margin-left:100px;
margin-right:100px;
font-weight:600;
}

.footer {
text-align:right;
font-size:small;
margin-top:75px;
}

</style>

<div class="main">

<h2>spacetimeid</h2>

<p><q>spacetimeid</q> is very simple web application to encode and decode unique 64-bit numeric identifiers for a combined set of x, y and z coordinates.</p>

<p style="font-style:italic;">Another way to think about it is as a unique ID for any given point at a specific time anywhere on Earth.</p>

<a name="encode"></a>

<p>For example, the corner of <a href="http://aaronland.info/iamhere/#latitude=37.76483199999999&longitude=-122.419304&zoom=17">16th and Mission</a>, in San Francisco, at around midnight the night/morning of March 17, 2010 would be encoded like this:</p>

<div class="request">
<p>GET <a href="http://spacetimeid.appspot.com/encode/-122.419304/37.764832/1268809061">http://spacetimeid.appspot.com/encode/-122.419304/37.764832/1268809061</a></p>

<pre>
&lt;rsp stat="ok"&gt;
	&lt;spacetime y="37.764832" x="-122.419304" z="1268809061" id="4726418083411316312844298485971"/&gt;
&lt;/rsp&gt;
</pre>
</div>

<a name="decode"></a>

<p>To decode a unique ID back in to space and time coordinates, you'd do this:</p>

<div class="request">
<p>GET <a href="http://spacetimeid.appspot.com/decode/4726418083411316312844298485971">http://spacetimeid.appspot.com/decode/4726418083411316312844298485971</a></p>

<pre>
&lt;rsp stat="ok"&gt;
	&lt;spacetime y="37.764832" x="-122.419304" z="1268809061" id="4726418083411316312844298485971"/&gt;
&lt;/rsp&gt;
</pre>
</div>

<a name="woe"></a>

<p>You can also encode <a href="http://geobloggers.com/2008/05/12/yahoo-woe-where-on-earth-that-is-ids/">WOE IDs</a> and time by going to the <code>/woe</code> endpoint. Here is <a href="http://www.flickr.com/places/55970963">The Mission</a>, early morning of the 17th:</p>

<div class="request">

<p>GET <a href="http://spacetimeid.appspot.com/woe/encode/55970963/1268809061">http://spacetimeid.appspot.com/woe/encode/55970963/1268809061</a></p>

<pre>
&lt;rsp stat="ok"&gt;
	&lt;spacetime woeid="55970963" id="4236329328336141596" timestamp="1268809061"/&gt;
&lt;/rsp&gt;
</pre>
</div>

<p style="font-style:italic;">Decoding is the same but just make sure you go to <code>/woe/decode</code>.</p>

<a name="details"></a>

<h2 style="margin-top:50px;">some details</h2>

<ul>

<li><p>The IDs are clustered together along <a href="http://en.wikipedia.org/wiki/Hilbert_curve">Hilbert curve</a> using Steve Witham's <a href="http://www.tiac.net/~sw/2008/10/Hilbert/">Python libraries</a>. What's a <q>Hilbert curve</q> you ask? <a href="http://blog.notdot.net/2009/11/Damn-Cool-Algorithms-Spatial-indexing-with-Quadtrees-and-Hilbert-Curves">Nick Johnson</a> describes them this way:</p>

<blockquote>
<p style="font-style:italic;">Suppose instead, we visit regions in a 'U' shape. Within each quad, of course, we also visit subquads in the same 'U' shape, but aligned so as to match up with neighbouring quads. If we organise the orientation of these 'U's correctly, we can completely eliminate any discontinuities, and visit the entire area at whatever resolution we choose continuously, fully exploring each region before moving on to the next. Not only does this eliminate discontinuities, but it also improves the overall locality. The pattern we get if we do this may look familiar - it's a Hilbert Curve.</p>

</blockquote>

</li>

<li><p>x and y are assumed to be longitude and latitude coordinates, respectively. Because the Hilbert functions required positive integers longitudes are offset by 180 degrees and latitudes by 90. (This is just so you know what's happening in the black box, the inputs and outputs will always be plain old lat, lon points.) Both coordinates are rounded to 8 decimal points.</p></li>

<li><p>z is assumed to be a Unix timestamp which make the whole thing problematic for events before January 01, 1970. This is not a feature and is being investigated.</p></li>

<li><p>By default <q>spacetimeid</q> returns responses as XML. If you'd prefer JSON, just append <a href="http://spacetimeid.appspot.com/encode/-122.419304/37.764832/1268809061?format=json">?format=json</a> to your request.</p></li>

</ul>

<a name="reading"></a>

<h2 style="margin-top:50px;">further reading</h2>

<ul>
<li><p><a href="http://www.aaronland.info/weblog/2010/02/04/cheap/#spacetime">spacetimeid</a>, Aaron Straup Cope</a></p></li>

<li><p><a href="http://www.vicchi.org/2010/03/17/phi-lambda-and-slightly-embarassing-temporality/">Phi, Lambda and (Slightly Embarassing) Temporality</a>, Gary Gale</a></p></li>

<li><p><a href="http://www.slideshare.net/blackbeltjones/designing-for-spacetime-ixda08">Designing for Spacetime</a>, Matt Jones</a></p></li>

</ul>

<div class="footer">
spacetimeid is a thing made by <a href="http://www.aaronland.info/">aaron straup cope</a>.
</div>

</div>
""")

        return

class Encode(spacetime):

    def get(self, x, y, z):

        x = float(x)
        y = float(y)
        z = int(z)

        x2 = round(x, self.precision)
        y2 = round(y, self.precision)

        x2 += 180.
        y2 += 90.

        y2 = int(y2 * self.factor)
        x2 = int(x2 * self.factor)

        h = hilbert.Hilbert_to_int((x2, y2, z))

        self.api_ok(self.generate_response(x, y, z, h))
        return

class Decode(spacetime):

    def get(self, h):

        h = long(h)

        x, y, z = hilbert.int_to_Hilbert(h, 3)

        x = x / self.factor
        y = y / self.factor

        x -= 180.
        y -= 90.

        self.api_ok(self.generate_response(x, y, z, h))
        return

class EncodeWOE(spacetimeWOE):

    def get(self, woeid, ts):

        woeid = int(woeid)
        ts = int(ts)

        h = hilbert.Hilbert_to_int((woeid, ts))

        self.api_ok(self.generate_response(woeid, ts, h))
        return

class DecodeWOE(spacetimeWOE):

    def get(self, h):

        h = long(h)

        woeid, ts = hilbert.int_to_Hilbert(h, 2)

        self.api_ok(self.generate_response(woeid, ts, h))
        return

class EncodeIP(spacetimeIP):

    def get(self, addr, ts):

        addr_int = self.iptoint(addr)
        ts = int(ts)

        h = hilbert.Hilbert_to_int((addr_int, ts))

        self.api_ok(self.generate_response(addr_int, ts, h))
        return

class DecodeIP(spacetimeIP):

    def get(self, h):

        h = long(h)

        addr_int, ts = hilbert.int_to_Hilbert(h, 2)
        addr = self.inttoip(addr_int)

        self.api_ok(self.generate_response(addr, ts, h))
        return


