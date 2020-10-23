/*
SQLyog Community v13.1.2 (64 bit)
MySQL - 5.5.62 : Database - smartdata
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`smartdata` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `smartdata`;

/*Table structure for table `email` */

DROP TABLE IF EXISTS `email`;

CREATE TABLE `email` (
  `eid` int(40) NOT NULL AUTO_INCREMENT,
  `subject` varchar(255) DEFAULT NULL,
  `body` varchar(255) DEFAULT NULL,
  `sender` varchar(255) DEFAULT NULL,
  `recipients` varchar(255) DEFAULT NULL,
  `created_by` int(20) DEFAULT NULL,
  `created_at` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`eid`),
  KEY `email_ibfk_2` (`created_by`),
  CONSTRAINT `email_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=latin1;

/*Data for the table `email` */

insert  into `email`(`eid`,`subject`,`body`,`sender`,`recipients`,`created_by`,`created_at`) values 
(36,'Welcome mail','Hello Greeting smart data','praful','[\'praful.rathore@ojas-it.com\', \'madan.rebbavarapu@ojas-it.com\']',1,'2020-10-22 19:22:50');

/*Table structure for table `email_status` */

DROP TABLE IF EXISTS `email_status`;

CREATE TABLE `email_status` (
  `sid` int(50) NOT NULL AUTO_INCREMENT,
  `email_id` int(255) DEFAULT NULL,
  `recipient` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT 'pending',
  `sent_at` datetime DEFAULT NULL,
  `flag` varchar(255) DEFAULT 'active',
  PRIMARY KEY (`sid`),
  KEY `email_id` (`email_id`),
  CONSTRAINT `email_status_ibfk_1` FOREIGN KEY (`email_id`) REFERENCES `email` (`eid`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;

/*Data for the table `email_status` */

insert  into `email_status`(`sid`,`email_id`,`recipient`,`status`,`sent_at`,`flag`) values 
(23,36,'praful.rathore@ojas-it.com','sent','2020-10-22 19:49:19','active'),
(24,36,'madan.rebbavarapu@ojas-it.com','sent','2020-10-22 19:49:24','active');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(30) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `mailid` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created_at` varchar(255) DEFAULT NULL,
  `flag` varchar(30) DEFAULT 'active',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`id`,`username`,`mailid`,`password`,`created_at`,`flag`) values 
(1,'praful','praful.rathore@ojas-it.com','praful.rathore@ojas-it.com','2020/10/22 16:01:47','active'),
(2,'vikash','vikash.gupta@ojas-it.com','vikash.gupta@ojas-it.com','2020/10/22 16:02:15','active'),
(3,'madan','madan.singh@ojas-it.com','madan.singh@ojas-it.com','2020/10/22 16:02:32','active'),
(4,'kiran','kiran.koti@ojas-it.com','kiran.koti@ojas-it.com','2020/10/22 16:02:53','active'),
(5,'ojas','classroommanagementapp@gmail.com','classroommanagementapp@gmail.com','2020/10/22 16:39:58','active');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
