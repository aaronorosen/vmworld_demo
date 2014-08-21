<?php
	include "dbConfig.php";

	$lastContentId = 0;

	function on_error($errStr) {
		echo json_encode(array(
			"status" => "Error",
			"error" => $errStr
		));

		exit;
	}

	$ajaxData = array(
		"status" => "OK"
	);

	if (isset($_GET['lastContentId'])) {
		$lastContentId = intval($_GET['lastContentId']);
	}

	if (!$lastContentId || $lastContentId < 0) {
		$lastContentId = 0;
	}

	$querySQL = "SELECT *
                  FROM call_entry
                 WHERE id > {$lastContentId}
                 LIMIT " . MIN_ROWS;

	$result = mysql_query($querySQL) or die(mysql_error());

	$ajaxData['rows'] = array();
	$lastId = $lastContentId;

	while ($row = mysql_fetch_assoc($result)) {
		$ajaxData['rows'][] = $row;
		$lastId = $row['id'];
	}

	while (count($ajaxData['rows']) < MIN_ROWS) {
		$ajaxData['rows'][] = array(
			"id" => $lastId,
			"phone_number" => "&nbsp;",
			"hostname" => "&nbsp;",
			"created_at" => "&nbsp;"
		);
	}

	echo json_encode($ajaxData);
?>
