-- MySQL dump 10.15  Distrib 10.0.13-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: ops
-- ------------------------------------------------------
-- Server version	10.0.13-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `action`
--

DROP TABLE IF EXISTS `action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `action` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `path` varchar(32) NOT NULL,
  `set_id` int(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=161 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `action`
--

LOCK TABLES `action` WRITE;
/*!40000 ALTER TABLE `action` DISABLE KEYS */;
INSERT INTO `action` VALUES (56,'维护','lstx_maintain_salt.sh',14);
/*!40000 ALTER TABLE `action` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `user_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1);
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment_history`
--

DROP TABLE IF EXISTS `comment_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment_history` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `server_id` varchar(128) NOT NULL,
  `comment` varchar(256) NOT NULL,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=271 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_history`
--

LOCK TABLES `comment_history` WRITE;
/*!40000 ALTER TABLE `comment_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `domain_info`
--

DROP TABLE IF EXISTS `domain_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain_info` (
  `domain_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '域名ID',
  `domain_name` varchar(64) NOT NULL COMMENT '主域名',
  `project_name` varchar(64) DEFAULT NULL COMMENT '项目名称',
  `ip_source` varchar(16) DEFAULT NULL COMMENT '源IP',
  `status` varchar(64) DEFAULT NULL COMMENT '域名状态',
  `cdn_hightanti` varchar(64) DEFAULT NULL COMMENT '解析是CDN or 高防',
  `pre_domain_id` int(11) NOT NULL DEFAULT '0' COMMENT '父域ID，顶级域名为0',
  `fuction` varchar(255) DEFAULT NULL COMMENT '用途',
  `comments` varchar(255) DEFAULT NULL COMMENT '备注',
  `is_public` int(11) NOT NULL DEFAULT '0' COMMENT '开放给运营',
  `register` varchar(64) DEFAULT NULL COMMENT '注册商',
  `register_date` datetime DEFAULT NULL COMMENT '注册时间',
  `expiration` datetime DEFAULT NULL COMMENT '过期时间',
  `init_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据创建时间',
  `dml_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据最后修改时间',
  `dml_flag` tinyint(4) NOT NULL DEFAULT '1' COMMENT '数据操作标识: 1-新增;2-修改;3-删除',
  PRIMARY KEY (`domain_id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8 COMMENT='域名信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domain_info`
--

LOCK TABLES `domain_info` WRITE;
/*!40000 ALTER TABLE `domain_info` DISABLE KEYS */;
INSERT INTO `domain_info` VALUES (1,'the1room.com','V项目',NULL,'已解析',NULL,0,NULL,NULL,0,NULL,NULL,NULL,'2015-09-21 14:53:00','2015-09-22 19:14:05',1),(2,'the1room.info','V项目',NULL,'已解析',NULL,0,NULL,NULL,0,NULL,NULL,NULL,'2015-09-21 14:53:00','2015-09-22 19:14:10',1),(43,'www','',NULL,NULL,'Voxility',2,NULL,NULL,0,NULL,NULL,NULL,'2015-09-21 01:10:28','2015-09-22 19:14:12',2),(44,'v','',NULL,NULL,'Voxility',2,NULL,NULL,0,NULL,NULL,NULL,'2015-09-21 01:10:28','2015-09-23 00:04:41',2);
/*!40000 ALTER TABLE `domain_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET gbk NOT NULL,
  `gm_url` varchar(256) DEFAULT NULL,
  `type` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES (1,'乱世天下-泰语',NULL,NULL);
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prvlg_prj`
--

DROP TABLE IF EXISTS `prvlg_prj`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prvlg_prj` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int(11) unsigned NOT NULL,
  `user_id` int(11) unsigned NOT NULL,
  `read` tinyint(4) DEFAULT '0',
  `write` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `project_id_idx` (`project_id`),
  KEY `user_id_idx` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=278 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prvlg_prj`
--

LOCK TABLES `prvlg_prj` WRITE;
/*!40000 ALTER TABLE `prvlg_prj` DISABLE KEYS */;
INSERT INTO `prvlg_prj` VALUES (1,1,1,1,1),(2,2,1,1,1),(3,3,1,1,1),(4,4,1,1,1),(5,5,1,1,1),(6,6,1,1,1),(7,7,1,1,1),(8,8,1,1,1),(9,9,1,1,1),(10,10,1,1,1),(11,11,1,1,1),(12,12,1,1,1),(13,13,1,1,1),(14,14,1,1,1),(15,15,1,1,1),(16,16,1,1,1),(17,17,1,1,1),(18,18,1,1,1),(19,19,1,1,1),(20,20,1,1,1),(21,21,1,1,1),(22,22,1,1,1),(23,23,1,1,1),(24,24,1,1,1),(25,25,1,1,1),(26,26,1,1,1),(27,27,1,1,1),(28,28,1,1,1),(29,29,1,1,1),(30,30,1,1,1),(31,31,1,1,1),(32,32,1,1,1),(33,33,1,1,1),(34,34,1,1,1),(35,35,1,1,1),(36,36,1,1,1),(37,37,1,1,1),(38,38,1,1,1),(39,39,1,1,1),(40,40,1,1,1),(41,41,1,1,1),(42,42,1,1,1),(43,43,1,1,1),(129,43,11,1,1),(128,42,11,1,1),(127,41,11,1,1),(126,40,11,1,1),(125,39,11,1,1),(124,38,11,1,1),(123,37,11,1,1),(122,36,11,1,1),(121,35,11,1,1),(120,34,11,1,1),(119,33,11,1,1),(118,32,11,1,1),(117,31,11,1,1),(116,30,11,1,1),(115,29,11,1,1),(114,28,11,1,1),(113,27,11,1,1),(112,26,11,1,1),(111,25,11,1,1),(110,24,11,1,1),(109,23,11,1,1),(108,22,11,1,1),(107,21,11,1,1),(106,20,11,1,1),(105,19,11,1,1),(104,18,11,1,1),(103,17,11,1,1),(102,16,11,1,1),(101,15,11,1,1),(100,14,11,1,1),(99,13,11,1,1),(98,12,11,1,1),(97,11,11,1,1),(96,10,11,1,1),(95,9,11,1,1),(94,8,11,1,1),(93,7,11,1,1),(92,6,11,1,1),(91,5,11,1,1),(90,4,11,1,1),(89,3,11,1,1),(88,2,11,1,1),(87,1,11,1,1),(130,1,9,1,1),(131,2,9,1,1),(132,3,9,1,1),(133,4,9,1,1),(134,5,9,1,1),(135,6,9,1,1),(136,7,9,1,1),(137,8,9,1,1),(138,9,9,1,1),(139,10,9,1,1),(140,11,9,1,1),(141,12,9,1,1),(142,13,9,1,1),(143,14,9,1,1),(144,15,9,1,1),(145,16,9,1,1),(146,17,9,1,1),(147,18,9,1,1),(148,19,9,1,1),(149,20,9,1,1),(150,21,9,1,1),(151,22,9,1,1),(152,23,9,1,1),(153,24,9,1,1),(154,25,9,1,1),(155,26,9,1,1),(156,27,9,1,1),(157,28,9,1,1),(158,29,9,1,1),(159,30,9,1,1),(160,31,9,1,1),(161,32,9,1,1),(162,33,9,1,1),(163,34,9,1,1),(164,35,9,1,1),(165,36,9,1,1),(166,37,9,1,1),(167,38,9,1,1),(168,39,9,1,1),(169,40,9,1,1),(170,41,9,1,1),(171,42,9,1,1),(172,43,9,1,1),(173,1,10,1,1),(174,2,10,1,1),(175,3,10,1,1),(176,4,10,1,1),(177,5,10,1,1),(178,6,10,1,1),(179,7,10,1,1),(180,8,10,1,1),(181,9,10,1,1),(182,10,10,1,1),(183,11,10,1,1),(184,12,10,1,1),(185,13,10,1,1),(186,14,10,1,1),(187,15,10,1,1),(188,16,10,1,1),(189,17,10,1,1),(190,18,10,1,1),(191,19,10,1,1),(192,20,10,1,1),(193,21,10,1,1),(194,22,10,1,1),(195,23,10,1,1),(196,24,10,1,1),(197,25,10,1,1),(198,26,10,1,1),(199,27,10,1,1),(200,28,10,1,1),(201,29,10,1,1),(202,30,10,1,1),(203,31,10,1,1),(204,32,10,1,1),(205,33,10,1,1),(206,34,10,1,1),(207,35,10,1,1),(208,36,10,1,1),(209,37,10,1,1),(210,38,10,1,1),(211,39,10,1,1),(212,40,10,1,1),(213,41,10,1,1),(214,42,10,1,1),(215,43,10,1,1),(216,44,1,1,1),(217,44,11,1,1),(218,44,9,1,1),(219,1,12,1,0),(220,2,12,1,0),(221,3,12,1,0),(222,4,12,1,0),(223,5,12,1,0),(224,6,12,1,1),(225,7,12,1,1),(226,8,12,1,0),(227,9,12,1,0),(228,10,12,1,0),(229,11,12,1,0),(230,12,12,1,0),(231,13,12,1,0),(232,14,12,1,0),(233,15,12,1,0),(234,16,12,1,0),(235,17,12,1,0),(236,18,12,1,0),(237,19,12,1,0),(238,20,12,1,1),(239,21,12,1,0),(240,22,12,1,0),(241,23,12,1,1),(242,24,12,1,0),(243,25,12,1,0),(244,26,12,1,0),(245,27,12,1,0),(246,28,12,1,1),(247,29,12,1,0),(248,30,12,1,0),(249,31,12,1,0),(250,32,12,1,0),(251,33,12,1,0),(252,34,12,1,0),(253,35,12,1,0),(254,36,12,1,1),(255,37,12,1,0),(256,38,12,1,0),(257,39,12,1,1),(258,40,12,1,0),(259,41,12,1,0),(260,42,12,1,0),(261,43,12,1,0),(262,44,12,1,0),(268,48,1,1,1),(264,46,1,1,1),(265,46,11,1,1),(266,46,10,1,1),(267,47,1,1,1),(269,48,12,1,1),(270,49,1,1,1),(271,49,10,1,1),(272,50,1,1,1),(273,49,12,1,1),(274,47,11,1,1),(275,50,12,1,1),(276,51,1,1,1),(277,51,12,1,1);
/*!40000 ALTER TABLE `prvlg_prj` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prvlg_set`
--

DROP TABLE IF EXISTS `prvlg_set`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prvlg_set` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `set_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `init` tinyint(3) unsigned NOT NULL,
  `merge` tinyint(3) unsigned NOT NULL,
  `upgrade` tinyint(3) unsigned NOT NULL,
  `reboot` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=60 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prvlg_set`
--

LOCK TABLES `prvlg_set` WRITE;
/*!40000 ALTER TABLE `prvlg_set` DISABLE KEYS */;
INSERT INTO `prvlg_set` VALUES (36,17,11,0,0,1,0),(40,21,11,0,0,0,1),(7,7,9,1,1,1,1),(49,30,12,0,0,0,1),(51,32,10,0,0,1,0),(50,31,12,0,0,0,1),(48,29,11,0,0,0,1),(12,7,11,1,1,1,1),(39,20,11,0,0,0,1),(35,16,11,0,0,0,1),(15,7,10,0,1,1,1),(34,15,11,0,0,1,0),(42,23,11,0,0,0,1),(47,28,11,0,0,0,1),(38,19,11,0,0,1,0),(33,14,10,0,0,0,1),(21,10,10,0,0,0,1),(22,11,10,0,0,0,1),(23,12,11,0,0,1,0),(24,13,11,0,0,1,0),(25,13,1,0,0,1,0),(26,12,1,1,1,1,1),(27,11,1,0,0,0,1),(28,10,1,0,0,0,1),(41,22,10,0,0,0,1),(31,7,1,0,0,0,1),(37,18,11,0,0,0,1),(53,34,11,0,0,1,0),(54,35,11,0,0,1,0),(56,37,11,0,0,0,1),(57,38,11,0,0,1,0),(58,39,11,0,0,0,1),(59,40,11,0,0,0,1);
/*!40000 ALTER TABLE `prvlg_set` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salt_returns`
--

DROP TABLE IF EXISTS `salt_returns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `salt_returns` (
  `job_id` varchar(255) NOT NULL,
  `minion_id` varchar(255) NOT NULL,
  `fun` varchar(50) NOT NULL,
  `success` varchar(10) NOT NULL,
  `return` mediumtext NOT NULL,
  `full_ret` mediumtext NOT NULL,
  `operation_id` varchar(32) NOT NULL,
  `user_id` int(11) NOT NULL,
  `start_time` varchar(64) NOT NULL,
  `alter_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `action` varchar(256) DEFAULT NULL,
  `project_id` int(10) NOT NULL,
  `set_id` int(10) NOT NULL,
  PRIMARY KEY (`job_id`),
  UNIQUE KEY `job_id_UNIQUE` (`job_id`),
  KEY `id` (`minion_id`),
  KEY `jid` (`job_id`),
  KEY `fun` (`fun`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salt_returns`
--

LOCK TABLES `salt_returns` WRITE;
/*!40000 ALTER TABLE `salt_returns` DISABLE KEYS */;
/*!40000 ALTER TABLE `salt_returns` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server`
--

DROP TABLE IF EXISTS `server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server` (
  `id` varchar(128) NOT NULL,
  `domain` varchar(64) DEFAULT NULL,
  `stat` varchar(16) DEFAULT NULL,
  `ip_ex` varchar(16) DEFAULT NULL,
  `ip_in` varchar(16) NOT NULL DEFAULT '',
  `host_ip` varchar(16) DEFAULT NULL,
  `project_id` int(11) unsigned DEFAULT NULL,
  `idc` varchar(64) DEFAULT NULL,
  `usages` varchar(128) DEFAULT NULL,
  `os` varchar(32) DEFAULT NULL,
  `cpu` varchar(32) DEFAULT NULL,
  `memory` varchar(32) DEFAULT NULL,
  `disk` varchar(32) DEFAULT NULL,
  `pool` varchar(32) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `visible` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `domain` (`domain`),
  KEY `ip_ex` (`ip_ex`),
  KEY `host_ip` (`host_ip`),
  KEY `comment` (`comment`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server`
--

LOCK TABLES `server` WRITE;
/*!40000 ALTER TABLE `server` DISABLE KEYS */;
INSERT INTO `server` VALUES ('7180','cos-test2.gameree.com','上线','10.30.40.243','10.30.40.243','10.30.40.43',1,'TJHY','WEB/DB','CentOS6.3x86_64','2','6','100G','自研',NULL,'2014-09-11 04:46:30',1),('7256','cos-s1.gameree.com','上线','218.213.165.192','10.52.33.192','10.52.33.47',1,'HKNTT','WEB/DB','CentOS6.3x86_64','4','12','200G','自研',NULL,'2014-09-11 04:46:30',1),('7257','cos-s12.gameree.com','上线','218.213.165.193','10.52.33.193','10.52.33.48',1,'HKNTT','WEB/DB','CentOS6.3x86_64','4','16','200G','自研',NULL,'2014-09-11 04:46:30',1);
/*!40000 ALTER TABLE `server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_set`
--

DROP TABLE IF EXISTS `server_set`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_set` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `server_id` int(10) NOT NULL,
  `set_id` int(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=198 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_set`
--

LOCK TABLES `server_set` WRITE;
/*!40000 ALTER TABLE `server_set` DISABLE KEYS */;
INSERT INTO `server_set` VALUES (1,7493,1),(2,7490,1),(3,7491,1),(4,8167,1),(5,7493,2),(6,7491,2),(7,7493,3),(8,7491,3),(9,7493,4),(10,7491,4),(11,7493,5),(12,7491,5),(13,7490,6),(14,7491,6),(15,8106,7),(16,7494,7),(17,9103,7),(18,8616,8),(19,9497,8),(20,7490,9),(21,7491,9),(22,8040,10),(23,7713,10),(24,7257,10),(25,7714,10),(26,9107,10),(27,7256,10),(28,8040,11),(29,7713,11),(30,7257,11),(31,7714,11),(32,9107,11),(33,7256,11),(34,7926,12),(35,9498,12),(36,9109,12),(37,9104,12),(38,8332,12),(39,8616,12),(40,8163,12),(41,9497,12),(42,7926,13),(43,9498,13),(44,9109,13),(45,9104,13),(46,8332,13),(47,8616,13),(48,8163,13),(49,9497,13),(50,8040,14),(51,7713,14),(52,7257,14),(53,7714,14),(54,9107,14),(55,7256,14),(56,7483,15),(57,8723,16),(58,7673,16),(59,8706,16),(60,8723,17),(61,7673,17),(62,8706,17),(63,7704,18),(64,7253,18),(65,6807,18),(66,9105,18),(67,8107,18),(68,6523,18),(69,6522,18),(70,9711,18),(71,7553,19),(72,7551,19),(73,7543,20),(74,7926,21),(75,9498,21),(76,9610,21),(77,9109,21),(78,9104,21),(79,8332,21),(80,8616,21),(81,8163,21),(82,9497,21),(83,8040,22),(84,7713,22),(85,7257,22),(86,7714,22),(87,9107,22),(88,7256,22),(89,8332,23),(90,8163,23),(91,9104,23),(92,9109,23),(93,8332,24),(94,8163,24),(95,8616,24),(96,9498,25),(97,7925,25),(98,7543,25),(99,9610,26),(100,9499,27),(101,8723,27),(102,7673,27),(103,8706,27),(104,9499,28),(105,8723,28),(106,7673,28),(107,8706,28),(108,8167,29),(109,9108,29),(110,7936,29),(111,9106,29),(112,8168,29),(113,9103,29),(114,8984,29),(115,9761,29),(116,7294,29),(117,7599,29),(118,7716,29),(119,7493,29),(120,7490,29),(121,7491,29),(122,7494,29),(123,8766,29),(124,7736,29),(125,8523,30),(126,8348,30),(127,8170,31),(128,9240,31),(129,8169,31),(130,8392,31),(131,8393,31),(132,7944,31),(133,9713,31),(134,9005,31),(135,8348,31),(136,8699,31),(137,7978,31),(138,8523,31),(139,7977,31),(140,8116,31),(141,8114,31),(142,8524,31),(143,7498,31),(144,7497,31),(145,7495,31),(146,7774,31),(147,7773,31),(148,8921,31),(149,7352,31),(150,7347,32),(151,9791,32),(152,9003,32),(153,7789,32),(154,8275,32),(155,7406,32),(156,6480,32),(157,8040,33),(158,7713,33),(159,9731,34),(160,9731,35),(161,8377,36),(162,9109,36),(163,9104,36),(164,9498,36),(165,8616,36),(166,9741,36),(167,9497,36),(168,9498,37),(169,9104,37),(170,8616,37),(171,9741,37),(172,9731,38),(173,9730,38),(174,9494,38),(175,9728,38),(176,8167,39),(177,9108,39),(178,7936,39),(179,9106,39),(180,8168,39),(181,9103,39),(182,9744,39),(183,8984,39),(184,9761,39),(185,7294,39),(186,9714,39),(187,7599,39),(188,7716,39),(189,7493,39),(190,7490,39),(191,7491,39),(192,7494,39),(193,8766,39),(194,7736,39),(195,8723,40),(196,7673,40),(197,8706,40);
/*!40000 ALTER TABLE `server_set` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `set`
--

DROP TABLE IF EXISTS `set`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `set` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `project_id` int(10) unsigned NOT NULL,
  `create_userid` int(10) unsigned DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `set`
--

LOCK TABLES `set` WRITE;
/*!40000 ALTER TABLE `set` DISABLE KEYS */;
INSERT INTO `set` VALUES (10,'乱世天下-泰语-维护',1,NULL,'2014-08-13 08:51:25'),(11,'乱世天下-泰语-维护1',1,NULL,'2014-08-13 08:51:25'),(22,'乱世天下-泰语-维护3',1,NULL,'2014-08-13 08:51:25');
/*!40000 ALTER TABLE `set` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(16) NOT NULL,
  `password` varchar(64) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','B96D4F26CF3B6B9FCC732941BB283460','2014-07-25 09:45:34',0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-09-23  0:36:54
