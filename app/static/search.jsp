<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1"/>
<meta name="description" content="description"/>
<meta name="keywords" content="keywords"/> 
<meta name="author" content="author"/> 
<link rel="stylesheet" type="text/css" href="default.css" media="screen"/>
<link rel="icon" href="http://img.wezhan.cn/80935_favicon.ico" />
<title>Promotions Service: NYU DevOps Fall 2017</title>
</head>

<body>

<div class="container">

	<div class="header">		
		<div class="title">
			<h1>Promotions Service</h1>	
		</div>
		<div class="navigation">
			<a href="index.html">Home Page</a>
			<div class="clearer"><span></span></div>
		</div>
	</div>

	<div class="main">		
		<div class="content">			
			<!--table border="0" align=center-left-->
				<tr><td>
				<h1>List, Query, Read, Actions</h1>
				<div class="descr">This part includes all test scenarios other than Create, Update, Delete.</div>
				</td></tr>
				<br>
				
				<tr><td>
				<h2>1. List All Promotions</h2>
				<form action="http://nyu-promotion-service-f17.mybluemix.net/promotions">
					<tr align=center>
						<td>
						<input type="submit" value="SEARCH" class="button" onclick="infosub()"/>
						<input type="reset" value="CANCLE" class="button" />
						</td>
					</tr>
				</form>
				<br>
				
				<h2>2. Get Promotion with ID</h2>
				<div class="descr">Type in any existing or valid format promotion ID to test. </div>
				<form action="error.jsp">	
					<ul>
						<li>Search by promotion ID</li>
						<input type="text" name="URL of NVR" class="style" /><input type="submit" value="SUBMIT" class="button" onclick="infosub()"/><input type="reset" value="CANCLE" class="button" />
						<br><br>
						<li>Search by promotion type</li>
						<input type="text" name="URL of NVR" class="style" /><input type="submit" value="SUBMIT" class="button" onclick="infosub()"/><input type="reset" value="CANCLE" class="button" />
						<br><br>
						<li>Search by promotion name </li>
						<input type="text" name="URL of NVR" class="style" /><input type="submit" value="SUBMIT" class="button" onclick="infosub()"/><input type="reset" value="CANCLE" class="button" />
						<br><br>
					</ul>
				</form>	
				
				<h2>3. Get Promotion with Invalid ID</h2>
				<div class="descr">Type in any invalid promotion ID to test. </div>
				<form action="error.jsp">
					<p>Search by ID: </p>
					<input type="text" name="URL of NVR" class="style" />
					<br><br>
					<input type="submit" value="SEARCH" class="button" onclick="infosub()"/>
					<input type="reset" value="CANCLE" class="button" />
				</form>
				<br>
				
				<h2>4. (Action) Delete All Promotions in Promotion Service</h2>
				<div class="descr">All promotioedns are list below. </div>
				<form action="error.jsp">
					<input type="text" name="URL of NVR" class="style" />
					
					<br><br>
					<input type="submit" value="DELETE ALL" class="button" onclick="infosub()"/>
					<input type="reset" value="CANCLE" class="button"/>
				</form>
				</td>
				</tr>
				<br><br>
			<!--/table-->

		</div>

		<div class="sidenav">

			<h1>Quick Start</h1>
			<ul>
				<li><a href="create.jsp">Create a promotion with default characteristics</a></li>
				<li><a href="create.jsp">Create a promotion with incorrect header</a></li>
				<li><a href="update.jsp">Update a promotion with value</a></li>
				<li><a href="update.jsp">Update a promotion with promotion type</a></li>
				<li><a href="delete.jsp">Delete a promotion with valid ID</a></li>
				<li><a href="delete.jsp">Delete a promotion with invalid ID</a></li>
			</ul>

		</div>
	
		<div class="clearer">&nbsp;</div>

	</div>

</div>

<div class="footer">

	<div class="left">&copy; Developers: jzuhusky@nyu.edu, dy877@nyu.edu, dz1120@nyu.edu, jz2668@nyu.edu. This is a Fall2017 DevOps Project: Promotion Service. 
		<a href="search.jsp">[GO TO TOP] </a></div>
	<div class="clearer">&nbsp;</div>

</div>

</body>

</html>
