CREATE DATABASE  IF NOT EXISTS `reservasccs` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `reservasccs`;
-- MySQL dump 10.13  Distrib 5.5.41, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: agendador
-- ------------------------------------------------------
-- Server version	5.5.41-0ubuntu0.14.04.1

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
-- Table structure for table `agenda_departamento`
--

DROP TABLE IF EXISTS `agenda_departamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agenda_departamento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sigla` varchar(5) NOT NULL,
  `descricao` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agenda_departamento`
--

LOCK TABLES `agenda_departamento` WRITE;
/*!40000 ALTER TABLE `agenda_departamento` DISABLE KEYS */;
INSERT INTO `agenda_departamento` VALUES (1,'NFR','Departamento de Enfermagem'),(2,'CIF','Departamento de Fármacia'),(3,'NTR','Departamento de Nutrição'),(4,'SEC','Secretaria do CCS');
/*!40000 ALTER TABLE `agenda_departamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `agenda_espacofisico`
--

DROP TABLE IF EXISTS `agenda_espacofisico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agenda_espacofisico` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` longtext NOT NULL,
  `descricao` longtext NOT NULL,
  `capacidade` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agenda_espacofisico`
--

LOCK TABLES `agenda_espacofisico` WRITE;
/*!40000 ALTER TABLE `agenda_espacofisico` DISABLE KEYS */;
INSERT INTO `agenda_espacofisico` VALUES (1,'Auditório CCS Graduação','Auditório do CCS destinado as atividades gerais e de graduação.',0),(2,'Auditório CCS pós','Auditório do CCS da pós graduação, destinado as atividades da pós graduação.',0),(3,'LabInfo','Laboratório de Informática, local reservado a atividades que necessitam de computadores, 35 computadores.',35),(4,'Sala dos conselhos','Sala dos conselheiros destinado somente atividades administrativas.',0),(5,'Sala 922','Uma sala multiuso',0),(6,'Sala Técnicas alternativas','Uma sala com amplo espaço e colchetes.',0),(7,'Sala pos H1','Sala de pós graduação',0),(8,'Sala pos H2','uma sala no bloco H',0),(9,'Sala pos H3','Sala do bloco H',0),(10,'Sala pos H4','Sala multiuso bl H',0),(11,'Sala Reunião labinfo','Uma pequena sala de reuniões no bloco B',12);
/*!40000 ALTER TABLE `agenda_espacofisico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `agenda_espacofisico_eventosPermitidos`
--

DROP TABLE IF EXISTS `agenda_espacofisico_eventosPermitidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agenda_espacofisico_eventosPermitidos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `espacofisico_id` int(11) NOT NULL,
  `tipoevento_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `espacofisico_id` (`espacofisico_id`,`tipoevento_id`),
  KEY `agenda_espacofisico_eventosPermitidos_5db22fb2` (`espacofisico_id`),
  KEY `agenda_espacofisico_eventosPermitidos_ec3d0b1c` (`tipoevento_id`),
  CONSTRAINT `espacofisico_id_refs_id_d9aee2b7` FOREIGN KEY (`espacofisico_id`) REFERENCES `agenda_espacofisico` (`id`),
  CONSTRAINT `tipoevento_id_refs_id_688121d9` FOREIGN KEY (`tipoevento_id`) REFERENCES `agenda_tipoevento` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agenda_espacofisico_eventosPermitidos`
--

LOCK TABLES `agenda_espacofisico_eventosPermitidos` WRITE;
/*!40000 ALTER TABLE `agenda_espacofisico_eventosPermitidos` DISABLE KEYS */;
/*!40000 ALTER TABLE `agenda_espacofisico_eventosPermitidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `agenda_reserva`
--

DROP TABLE IF EXISTS `agenda_reserva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agenda_reserva` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `estado` varchar(1) NOT NULL,
  `dataUsoInicio` datetime NOT NULL,
  `dataUsoFim` datetime NOT NULL,
  `dataReserva` datetime NOT NULL,
  `espacoFisico_id` int(11) NOT NULL,
  `evento_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `ramal` smallint(5) unsigned NOT NULL,
  `departamento_id` int(11) NOT NULL,
  `finalidade` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `agenda_reserva_8698423a` (`espacoFisico_id`),
  KEY `agenda_reserva_80d1c397` (`evento_id`),
  KEY `agenda_reserva_c69e2c81` (`usuario_id`),
  KEY `agenda_reserva_cad1d7f2` (`departamento_id`),
  CONSTRAINT `espacoFisico_id_refs_id_d5470331` FOREIGN KEY (`espacoFisico_id`) REFERENCES `agenda_espacofisico` (`id`),
  CONSTRAINT `departamento_id_refs_id_abc178a5` FOREIGN KEY (`departamento_id`) REFERENCES `agenda_departamento` (`id`),
  CONSTRAINT `evento_id_refs_id_f89e9eb4` FOREIGN KEY (`evento_id`) REFERENCES `agenda_tipoevento` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agenda_reserva`
--

LOCK TABLES `agenda_reserva` WRITE;
/*!40000 ALTER TABLE `agenda_reserva` DISABLE KEYS */;
INSERT INTO `agenda_reserva` VALUES (1,'1','2015-01-29 12:00:00','2015-01-29 22:57:29','2015-01-29 22:57:52',3,1,2,1,1,'123');
/*!40000 ALTER TABLE `agenda_reserva` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `agenda_tipoevento`
--

DROP TABLE IF EXISTS `agenda_tipoevento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agenda_tipoevento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(30) NOT NULL,
  `descricao` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agenda_tipoevento`
--

LOCK TABLES `agenda_tipoevento` WRITE;
/*!40000 ALTER TABLE `agenda_tipoevento` DISABLE KEYS */;
INSERT INTO `agenda_tipoevento` VALUES (1,'Defesa TCC','Defesa de Trabalho de Conclusão de Curso ou monografia.'),(2,'Defesa Dissertação','Defesa de Dissertação nivel mestrado.'),(3,'Defesa de Tese','Defesa de Tese de Doutorado.'),(4,'Concurso Publico','Concurso Publico'),(5,'Reunião pedagogica','Reunião pedagogica'),(6,'Aula','Aula'),(7,'Reunião colegiado','Reunião colegiado'),(8,'Reunião grupo pesqusia','Reunião grupo pesqusia'),(9,'Capacitação','Capacitação'),(10,'Tutoria','Tutoria'),(11,'Seminario','Seminario');
/*!40000 ALTER TABLE `agenda_tipoevento` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_0e939a4f` (`group_id`),
  KEY `auth_group_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_417f1b1c` (`content_type_id`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add departamento',7,'add_departamento'),(20,'Can change departamento',7,'change_departamento'),(21,'Can delete departamento',7,'delete_departamento'),(22,'Can add tipo evento',8,'add_tipoevento'),(23,'Can change tipo evento',8,'change_tipoevento'),(24,'Can delete tipo evento',8,'delete_tipoevento'),(25,'Can add espaco fisico',9,'add_espacofisico'),(26,'Can change espaco fisico',9,'change_espacofisico'),(27,'Can delete espaco fisico',9,'delete_espacofisico'),(28,'Can add reserva',10,'add_reserva'),(29,'Can change reserva',10,'change_reserva'),(30,'Can delete reserva',10,'delete_reserva');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$12000$Rhivb6g4gbT4$0JfcPGCWBjeNlOS6C2XqM4Xe66OQvsF7ACxigxEyqtw=','2015-01-29 23:03:11',1,'admin','','','ramon.rdm@ufsc.br',1,1,'2015-01-29 22:53:11'),(2,'pbkdf2_sha256$12000$vz5WKBCwodRM$LW59+xewxkWmwOu634BWsXkb+2Le7DVNmVOfKdOu25E=','2015-01-29 23:01:00',0,'ramon.rdm','Ramon Dutra Miranda','100000000276770','ramon.rdm@ufsc.br',0,1,'2015-01-29 22:57:29');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_e8701ad4` (`user_id`),
  KEY `auth_user_groups_0e939a4f` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_e8701ad4` (`user_id`),
  KEY `auth_user_user_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissi_user_id_7f0938558328534a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_417f1b1c` (`content_type_id`),
  KEY `django_admin_log_e8701ad4` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'departamento','agenda','departamento'),(8,'tipo evento','agenda','tipoevento'),(9,'espaco fisico','agenda','espacofisico'),(10,'reserva','agenda','reserva');
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
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2015-01-29 22:52:55'),(2,'auth','0001_initial','2015-01-29 22:52:57'),(3,'admin','0001_initial','2015-01-29 22:52:58'),(4,'sessions','0001_initial','2015-01-29 22:52:58');
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
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('e06feo5mn0vqo2q8syjvnmoi897gi1ea','ZTQwYzA1MjEyMDQwZjAxYTI1YzEzNDAwOGI1MDVmYjNhZGNlNTExMjp7Il9hdXRoX3VzZXJfaGFzaCI6IjdiOWVjYWEzOWM1M2QyYTJmNDhlMDY1YTQwZGU5NjJiNWJkNWVmYjciLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOjF9','2015-02-12 23:03:11');
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

-- Dump completed on 2015-01-29 23:06:40
