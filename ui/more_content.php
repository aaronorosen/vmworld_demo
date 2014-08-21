<?php
	include "dbConfig.php";
	error_reporting(E_ALL);
	ini_set("display_errors", 1);
	echo "#$##$";
	echo $_POST['getLastContentId';
	if(isSet($_POST['getLastContentId'])) {
		$getLastContentId=$_POST['getLastContentId'];
		$result = mysql_query("select id, phone_number, created_at from call_entry where id < "
								     .$getLastContentId." order by id desc limit 10");

		$count = mysql_num_rows($result);
		if($count>0) {
		while($row = mysql_fetch_array($result)) {
			$id = $row['id'];
			$message = $row['phone_number'];
			echo "HERER";
?>

<li>
	<a href="<?=$row['url']?>.htm"><?php echo $message; ?></a>
</li>

<?php
	}
	echo "HERER";
?>

<a href="#"><div id="load_more_<?php echo $id; ?>" class="more_tab">
<div id="<?php echo $id; ?>" class="more_button">Load More Content</div></a>
</div>



<?php
	}
	else {
	echo "<div class='all_loaded'>No More Content to Load</div>";
	}
}
?>
