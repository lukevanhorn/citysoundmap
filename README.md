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
		<h4>Python</h4> 
		<p><pre style="background-color:#eee">
				#init
				serialport.write('\x10\x04\x0d')

				#poll
				serialport.write('\x30\x00\x0d')
			</p></pre>
		<p>
			The sound meter is polled continually, but only records data above the set threshold 70 dB(A) 
			<br/>
			If using the Camera Module, a photo or short video is also captured.
			<br/>
			The Raspberry Pi can also host a simple web interface to view the data by day.  Install apache or webserver of choice.  
			<br/>
			**note: The Pi user will need write permissions for the data, video and img directories in /var/www
		</p>
	</body>
</html>