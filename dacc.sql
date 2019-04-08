-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: agilecommandcentral
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.18.04.2

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add cors model',1,'add_corsmodel'),(2,'Can change cors model',1,'change_corsmodel'),(3,'Can delete cors model',1,'delete_corsmodel'),(4,'Can view cors model',1,'view_corsmodel'),(5,'Can add user',2,'add_user'),(6,'Can change user',2,'change_user'),(7,'Can delete user',2,'delete_user'),(8,'Can view user',2,'view_user'),(9,'Can add card',3,'add_card'),(10,'Can change card',3,'change_card'),(11,'Can delete card',3,'delete_card'),(12,'Can view card',3,'view_card'),(13,'Can add retro board items',4,'add_retroboarditems'),(14,'Can change retro board items',4,'change_retroboarditems'),(15,'Can delete retro board items',4,'delete_retroboarditems'),(16,'Can view retro board items',4,'view_retroboarditems'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add session member',6,'add_sessionmember'),(22,'Can change session member',6,'change_sessionmember'),(23,'Can delete session member',6,'delete_sessionmember'),(24,'Can view session member',6,'view_sessionmember'),(25,'Can add story',7,'add_story'),(26,'Can change story',7,'change_story'),(27,'Can delete story',7,'delete_story'),(28,'Can view story',7,'view_story'),(29,'Can add log entry',8,'add_logentry'),(30,'Can change log entry',8,'change_logentry'),(31,'Can delete log entry',8,'delete_logentry'),(32,'Can view log entry',8,'view_logentry'),(33,'Can add permission',9,'add_permission'),(34,'Can change permission',9,'change_permission'),(35,'Can delete permission',9,'delete_permission'),(36,'Can view permission',9,'view_permission'),(37,'Can add group',10,'add_group'),(38,'Can change group',10,'change_group'),(39,'Can delete group',10,'delete_group'),(40,'Can view group',10,'view_group'),(41,'Can add content type',11,'add_contenttype'),(42,'Can change content type',11,'change_contenttype'),(43,'Can delete content type',11,'delete_contenttype'),(44,'Can view content type',11,'view_contenttype'),(45,'Can add session',12,'add_session'),(46,'Can change session',12,'change_session'),(47,'Can delete session',12,'delete_session'),(48,'Can view session',12,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_card`
--

DROP TABLE IF EXISTS `core_card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_card` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `card` int(11) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `story_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_card_owner_id_9f93ca2a_fk_core_user_id` (`owner_id`),
  KEY `core_card_session_id_d5ac7b56_fk_core_session_id` (`session_id`),
  KEY `core_card_story_id_bbe13479_fk_core_story_id` (`story_id`),
  CONSTRAINT `core_card_owner_id_9f93ca2a_fk_core_user_id` FOREIGN KEY (`owner_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `core_card_session_id_d5ac7b56_fk_core_session_id` FOREIGN KEY (`session_id`) REFERENCES `core_session` (`id`),
  CONSTRAINT `core_card_story_id_bbe13479_fk_core_story_id` FOREIGN KEY (`story_id`) REFERENCES `core_story` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_card`
--

LOCK TABLES `core_card` WRITE;
/*!40000 ALTER TABLE `core_card` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_card` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_retroboarditems`
--

DROP TABLE IF EXISTS `core_retroboarditems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_retroboarditems` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `item_type` varchar(3) NOT NULL,
  `item_text` longtext NOT NULL,
  `owner_id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_retroboarditems_owner_id_3bc74954_fk_core_user_id` (`owner_id`),
  KEY `core_retroboarditems_session_id_61947ad8_fk_core_session_id` (`session_id`),
  CONSTRAINT `core_retroboarditems_owner_id_3bc74954_fk_core_user_id` FOREIGN KEY (`owner_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `core_retroboarditems_session_id_61947ad8_fk_core_session_id` FOREIGN KEY (`session_id`) REFERENCES `core_session` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_retroboarditems`
--

LOCK TABLES `core_retroboarditems` WRITE;
/*!40000 ALTER TABLE `core_retroboarditems` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_retroboarditems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_session`
--

DROP TABLE IF EXISTS `core_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(30) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `session_type` varchar(10) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `is_started` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_session_owner_id_a94e9794_fk_core_user_id` (`owner_id`),
  CONSTRAINT `core_session_owner_id_a94e9794_fk_core_user_id` FOREIGN KEY (`owner_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_session`
--

LOCK TABLES `core_session` WRITE;
/*!40000 ALTER TABLE `core_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_sessionmember`
--

DROP TABLE IF EXISTS `core_sessionmember`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_sessionmember` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `member_id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_sessionmember_member_id_774573e3_fk_core_user_id` (`member_id`),
  KEY `core_sessionmember_session_id_e7ed9022_fk_core_session_id` (`session_id`),
  CONSTRAINT `core_sessionmember_member_id_774573e3_fk_core_user_id` FOREIGN KEY (`member_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `core_sessionmember_session_id_e7ed9022_fk_core_session_id` FOREIGN KEY (`session_id`) REFERENCES `core_session` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_sessionmember`
--

LOCK TABLES `core_sessionmember` WRITE;
/*!40000 ALTER TABLE `core_sessionmember` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_sessionmember` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_story`
--

DROP TABLE IF EXISTS `core_story`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_story` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `story_points` int(11) DEFAULT NULL,
  `session_id` int(11) NOT NULL,
  `key` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_story_session_id_f556f306_fk_core_session_id` (`session_id`),
  CONSTRAINT `core_story_session_id_f556f306_fk_core_session_id` FOREIGN KEY (`session_id`) REFERENCES `core_session` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_story`
--

LOCK TABLES `core_story` WRITE;
/*!40000 ALTER TABLE `core_story` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_story` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user`
--

DROP TABLE IF EXISTS `core_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `username` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user`
--

LOCK TABLES `core_user` WRITE;
/*!40000 ALTER TABLE `core_user` DISABLE KEYS */;
INSERT INTO `core_user` VALUES (1,'',NULL,0,'','','kyleacapehart@knights.ucf.edu',0,1,'2019-03-23 02:27:48.233650','Kyle Capehart');
/*!40000 ALTER TABLE `core_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user_groups`
--

DROP TABLE IF EXISTS `core_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_groups_user_id_group_id_c82fcad1_uniq` (`user_id`,`group_id`),
  KEY `core_user_groups_group_id_fe8c697f_fk_auth_group_id` (`group_id`),
  CONSTRAINT `core_user_groups_group_id_fe8c697f_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `core_user_groups_user_id_70b4d9b8_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user_groups`
--

LOCK TABLES `core_user_groups` WRITE;
/*!40000 ALTER TABLE `core_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user_user_permissions`
--

DROP TABLE IF EXISTS `core_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_user_permissions_user_id_permission_id_73ea0daa_uniq` (`user_id`,`permission_id`),
  KEY `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` (`permission_id`),
  CONSTRAINT `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `core_user_user_permissions_user_id_085123d3_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user_user_permissions`
--

LOCK TABLES `core_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `core_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_core_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (8,'admin','logentry'),(10,'auth','group'),(9,'auth','permission'),(11,'contenttypes','contenttype'),(3,'core','card'),(4,'core','retroboarditems'),(5,'core','session'),(6,'core','sessionmember'),(7,'core','story'),(2,'core','user'),(1,'corsheaders','corsmodel'),(12,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2019-03-22 21:00:01.682671'),(2,'contenttypes','0002_remove_content_type_name','2019-03-22 21:00:01.759171'),(3,'auth','0001_initial','2019-03-22 21:00:01.982373'),(4,'auth','0002_alter_permission_name_max_length','2019-03-22 21:00:01.999173'),(5,'auth','0003_alter_user_email_max_length','2019-03-22 21:00:02.012296'),(6,'auth','0004_alter_user_username_opts','2019-03-22 21:00:02.026628'),(7,'auth','0005_alter_user_last_login_null','2019-03-22 21:00:02.037027'),(8,'auth','0006_require_contenttypes_0002','2019-03-22 21:00:02.040584'),(9,'auth','0007_alter_validators_add_error_messages','2019-03-22 21:00:02.094262'),(10,'auth','0008_alter_user_username_max_length','2019-03-22 21:00:02.104823'),(11,'auth','0009_alter_user_last_name_max_length','2019-03-22 21:00:02.118313'),(12,'core','0001_initial','2019-03-22 21:00:03.053613'),(13,'admin','0001_initial','2019-03-22 21:00:03.181985'),(14,'admin','0002_logentry_remove_auto_add','2019-03-22 21:00:03.207261'),(15,'admin','0003_logentry_add_action_flag_choices','2019-03-22 21:00:03.231022'),(16,'core','0002_story_key','2019-03-22 21:00:03.281573'),(17,'core','0003_session_is_started','2019-03-22 21:00:03.337925'),(18,'sessions','0001_initial','2019-03-22 21:00:03.376758');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-03-26 16:27:22
