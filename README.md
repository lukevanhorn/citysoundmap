<html>
<body>
<h2>City Sound Map</h2>
<p>
Sound Data Logger using the Raspberry Pi and a hacked digital sound meter and Pi Camera Module 
<br/>
<h4>Equipment</h4>
<br/>
<ul>
<li>Digital sound meter - (Tonda SL-814)</li>
<li>Raspberry pi</li>
<li>Camera module</li>
<li>Python script to record sound levels and image or video clips</li>
<li>Apache</li>
<li>d3.js</li>
</ul>
</p>
<p>
This project uses a modified Tonda SL-814 digital sound meter weighted for pressure level A.  The modifcations allow the meter to be powered from raspberry pi and remain in an always on state for continual polling. 
I purchased <a href="http://www.amazon.com/NEEWER%C2%AE-Digital-Sound-Level-Meter/dp/B005JX2EZ2">this model</a>   
<br/>
Though, I recommend <a href="http://www.amazon.com/Professional-Digital-Pressure-Measurement-Detectors/dp/B00LL3Y074">this one</a> as it comes with the special cable(non-standard USB), otherwise you'll have to modify a micro-usb cable.
</p>
<p>
The serial protocol has been reverse engineered and is available here:<br />
http://sigrok.org/wiki/Tondaj_SL-814
</p>
<p>
<h4>Initialize</h4> 
<p><pre>serialport.write('\x10\x04\x0d')</pre></p>
<h4>Poll</h4> 
<p><pre>serialport.write('\x30\x00\x0d')</pre></p>
</p>
<p>
The sound meter is polled continually, but only records data above the set threshold 70 dB(A) 
<br/><br/>
If using the Camera Module, a photo or short video is also captured.
<br/><br/>
The Raspberry Pi can also host a simple web interface to view the data.  Install apache or webserver of choice.  
<br/><br/>
**note: The Pi user will need write permissions for the data, video and img directories in /var/www
<br/><br/>
Demo: <a href="http://www.citysoundmap.org/demo.html">http://www.citysoundmap.org/demo.html</a> (data collected in Moab, UT August 2013).
<br/><br/>
Photos: <a href="http://www.citysoundmap.org/demo.html">http://www.citysoundmap.org</a>
</p>
<p>
<TABLE WIDTH=623 CELLPADDING=7 CELLSPACING=0>
	<COL WIDTH=298>
	<COL WIDTH=297>
	<TR VALIGN=TOP>
		<TD WIDTH=298 STYLE="border: none; padding: 0in">
			<P><IMG SRC="http://www.citysoundmap.org/SoundMap_html_m385bb6d7.jpg" NAME="graphics2" ALIGN=LEFT WIDTH=456 HEIGHT=262 BORDER=0><BR CLEAR=LEFT><BR>
			</P>
		</TD>
		<TD WIDTH=297 STYLE="border: none; padding: 0in">
			<P><IMG SRC="http://www.citysoundmap.org/SoundMap_html_m52855a9.jpg" NAME="graphics1" ALIGN=LEFT WIDTH=467 HEIGHT=262 BORDER=0><BR CLEAR=LEFT><BR>
			</P>
		</TD>
	</TR>
	<TR VALIGN=TOP>
		<TD WIDTH=298 STYLE="border: none; padding: 0in">
			<P><IMG SRC="http://www.citysoundmap.org/SoundMap_html_m78939703.png" NAME="graphics3" ALIGN=LEFT WIDTH=438 HEIGHT=250 BORDER=0><BR CLEAR=LEFT><BR>
			</P>
		</TD>
		<TD WIDTH=297 STYLE="border: none; padding: 0in">
			<P><IMG SRC="http://www.citysoundmap.org/SoundMap_html_7278ea41.png" NAME="graphics4" ALIGN=LEFT WIDTH=446 HEIGHT=269 BORDER=0><BR CLEAR=LEFT><BR>
			</P>
		</TD>
	</TR>
</TABLE>
</p>
</body>
</html>