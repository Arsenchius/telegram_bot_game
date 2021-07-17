<?php
$key    = $_POST['key'];
$type   = $_POST['type'];

if($key == "KeyPas") {
    include("db.php");
    switch($type) {
        case "auth":
            $login = $_POST['id'];
            $req = mysqli_query($db,"SELECT * FROM `arsen` WHERE `id_telegram` = '$login'");
            if(mysqli_num_rows($req) > 0) {
                $user = mysqli_fetch_array($req);
                echo json_encode([
                    "status"=> 200,
                    "name"  => $user['nick'],
                    "score" => $user['score'],
                    "id"    => $user['id'],
                ], JSON_UNESCAPED_UNICODE);
            } else {
                echo json_encode([
                    "status"    => 404,
                    "message"   => "Пользователь не найден"
                ],JSON_UNESCAPED_UNICODE);
            }
            exit();
            break;
        case "regi":
            $nick = $_POST['nick'];
            $id_ = $_POST['id'];

            if(mysqli_num_rows(mysqli_query($db,"SELECT `id` FROM `arsen` WHERE `id_telegram` = '$id_'")) == 0) { 
                if(mysqli_query($db,"INSERT INTO `arsen` (`id`, `nick`, `id_telegram`, `score`) VALUES (NULL, '$nick', '$id_', '0')")){
                    $id = mysqli_insert_id($db);
                    echo json_encode([
                        "status" => 200,
                        "id"    => $id
                    ]);
                    exit();
                }
            } else {
                echo json_encode([
                    "status" => 500,
                    "message"=> "Пользователь уже есть в системе"
                ],JSON_UNESCAPED_UNICODE);
            }
            exit();
            break;
        case "info":
            $id = $_POST['id'];
            $req = mysqli_query($db,"SELECT * FROM `arsen` WHERE `id` = '$id'");
            if(mysqli_num_rows($req) != 0) {
                $user = mysqli_fetch_array($req);
                echo json_encode([
                    "status" => 200,
                    "nick"   => $user['nick'],
                    "score"  => $user['score'],
                    "id"     => $user['id']
                ]);
            } else {
                echo json_encode([
                    "status" => 500,
                    "message"=> "Пользователь не найден"
                ],JSON_UNESCAPED_UNICODE);
            }
            break;
        case "updt":
            $id = $_POST['id'];
            $point = $_POST['up'];

            $user = mysqli_query($db,"SELECT * FROM `arsen` WHERE `id` = '$id'");
            if(mysqli_num_rows($user) > 0){
                $user = mysqli_fetch_array($user);
                $balance = (int)$user['score'];
                $balance += (int)$point;
                if(mysqli_query($db,"UPDATE `arsen` SET score = '$balance' WHERE `id` = '$id'")) {
                    echo json_encode([
                        "status"   => 200
                    ]);
                    exit();
                } else {
                    echo json_encode([
                        "status"    => 400,
                        "message"   => "Ошибка в изменение данных"
                    ]);
                }
            } else {
                echo json_encode([
                    "status"    => 404,
                    "message"   => 'Нет такого пользователя',
                ]);
            }
            break;
    }
}
?>