-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: 10.10.80.67    Database: talent_engine
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `T_HX_EMP_KPI`
--

DROP TABLE IF EXISTS `T_HX_EMP_KPI`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `T_HX_EMP_KPI` (
  `ID` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键ID',
  `KPI_YEAR` int DEFAULT NULL COMMENT '考核年度(建议改为INT4足够)',
  `EMP_NO` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '员工档案号',
  `EMP_NAME` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '员工姓名',
  `INSTITUTION_NO` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '机构编号',
  `INSTITUTION_NAME` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '机构名称',
  `JOB_NO` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '岗位编号',
  `JOB_NAME` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '岗位名称',
  `SCORE` decimal(6,2) DEFAULT NULL COMMENT 'KPI得分(保留2位小数)',
  `JOB_RANK` int DEFAULT NULL COMMENT '岗位排名',
  `JOB_TOTAL` int DEFAULT NULL COMMENT '岗位总人数',
  `REGION_RANK` int DEFAULT NULL COMMENT '区域排名',
  `REGION_TOTAL` int DEFAULT NULL COMMENT '区域总人数',
  `REMARK` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注信息',
  `CREATE_USER` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '记录创建人',
  `UPDATE_USER` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '记录修改人(与CREATE_USER长度一致)',
  `KPI_GRADE` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '绩效考核等级(A/B/C等)',
  `CREATE_TIME` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `UPDATE_TIME` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`ID`),
  KEY `idx_kpi_year_emp` (`KPI_YEAR`,`EMP_NO`),
  KEY `idx_institution_year` (`INSTITUTION_NO`,`KPI_YEAR`),
  KEY `idx_kpi_grade` (`KPI_GRADE`),
  KEY `idx_score` (`SCORE`),
  KEY `idx_job_rank` (`JOB_RANK`),
  KEY `idx_region_rank` (`REGION_RANK`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='员工绩效考核表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_HX_EMP_KPI`
--

/*!40000 ALTER TABLE `T_HX_EMP_KPI` DISABLE KEYS */;
INSERT INTO `T_HX_EMP_KPI` VALUES (1,2023,'EMP001','张伟','BJ001','北京总部','POS001','高级工程师',95.50,1,2,3,4,NULL,'admin','admin','A','2025-05-12 19:21:56','2025-05-12 19:22:45'),(2,2023,'EMP002','王芳','BJ001','北京总部','POS002','项目经理',88.00,2,2,8,4,NULL,'admin','admin','B+','2025-05-12 19:21:56','2025-05-12 19:22:45'),(3,2023,'EMP003','李娜','SH001','上海分公司','POS003','产品经理',92.30,1,1,5,2,NULL,'admin','admin','A','2025-05-12 19:21:56','2025-05-12 19:22:45'),(4,2023,'EMP004','刘强','GZ001','广州分公司','POS004','销售主管',85.70,3,1,15,1,NULL,'admin','admin','B','2025-05-12 19:21:56','2025-05-12 19:22:45'),(5,2023,'EMP005','陈静','SZ001','深圳分公司','POS005','UI设计师',89.20,2,1,12,1,NULL,'admin','admin','B+','2025-05-12 19:21:56','2025-05-12 19:22:45'),(6,2023,'EMP006','杨光','BJ001','北京总部','POS001','高级工程师',87.60,3,2,10,4,NULL,'admin','admin','B','2025-05-12 19:21:56','2025-05-12 19:22:45'),(7,2023,'EMP007','赵敏','SH001','上海分公司','POS002','项目经理',91.80,2,2,7,2,NULL,'admin','admin','A-','2025-05-12 19:21:56','2025-05-12 19:22:45'),(8,2023,'EMP008','周杰','CD001','成都分公司','POS006','测试工程师',83.40,5,1,20,1,NULL,'admin','admin','B-','2025-05-12 19:21:56','2025-05-12 19:22:45'),(9,2023,'EMP009','吴婷','HZ001','杭州分公司','POS007','数据分析师',94.10,1,1,4,1,NULL,'admin','admin','A','2025-05-12 19:21:56','2025-05-12 19:22:45'),(10,2023,'EMP010','郑浩','BJ001','北京总部','POS008','运维工程师',86.90,4,1,14,4,NULL,'admin','admin','B','2025-05-12 19:21:56','2025-05-12 19:22:45'),(11,2022,'EMP011','孙丽','BJ001','北京总部','POS002','项目经理',90.20,1,2,2,2,NULL,'admin','admin','A','2025-05-12 19:21:56','2025-05-12 19:22:45'),(12,2022,'EMP012','朱涛','SH001','上海分公司','POS003','产品经理',87.50,3,1,10,2,NULL,'admin','admin','B+','2025-05-12 19:21:56','2025-05-12 19:22:45'),(13,2022,'EMP013','胡月','GZ001','广州分公司','POS004','销售主管',82.10,5,2,18,2,NULL,'admin','admin','B-','2025-05-12 19:21:56','2025-05-12 19:22:45'),(14,2022,'EMP014','林峰','SZ001','深圳分公司','POS005','UI设计师',93.70,1,2,3,2,NULL,'admin','admin','A','2025-05-12 19:21:56','2025-05-12 19:22:45'),(15,2022,'EMP015','徐明','CD001','成都分公司','POS006','测试工程师',79.80,6,1,22,1,NULL,'admin','admin','C+','2025-05-12 19:21:56','2025-05-12 19:22:45'),(16,2022,'EMP016','高洁','HZ001','杭州分公司','POS007','数据分析师',89.60,2,1,8,1,NULL,'admin','admin','B+','2025-05-12 19:21:56','2025-05-12 19:22:45'),(17,2022,'EMP017','马超','BJ001','北京总部','POS001','高级工程师',91.30,2,1,5,2,NULL,'admin','admin','A-','2025-05-12 19:21:56','2025-05-12 19:22:45'),(18,2022,'EMP018','黄蓉','SH001','上海分公司','POS002','项目经理',84.70,4,2,15,2,NULL,'admin','admin','B','2025-05-12 19:21:56','2025-05-12 19:22:45'),(19,2022,'EMP019','曹阳','GZ001','广州分公司','POS004','销售主管',88.90,3,2,9,2,NULL,'admin','admin','B+','2025-05-12 19:21:56','2025-05-12 19:22:45'),(20,2022,'EMP020','邓辉','SZ001','深圳分公司','POS005','UI设计师',85.40,4,2,12,2,NULL,'admin','admin','B','2025-05-12 19:21:56','2025-05-12 19:22:45');
/*!40000 ALTER TABLE `T_HX_EMP_KPI` ENABLE KEYS */;

--
-- Table structure for table `T_HX_EMP_SPECIAL_SKILL`
--

DROP TABLE IF EXISTS `T_HX_EMP_SPECIAL_SKILL`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `T_HX_EMP_SPECIAL_SKILL` (
  `ID` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `EMP_NO` varchar(20) NOT NULL COMMENT '员工档案号',
  `EMP_NAME` varchar(50) NOT NULL COMMENT '员工姓名',
  `SKILL_TYPE` varchar(2) NOT NULL COMMENT '特长类别',
  `SKILL_NAME` varchar(100) NOT NULL COMMENT '特长项目',
  `SKILL_LEVEL` varchar(30) DEFAULT NULL COMMENT '特长级别/水平',
  `PERFORM_ORG` varchar(100) DEFAULT NULL COMMENT '认定单位',
  `BZ` varchar(30) DEFAULT NULL COMMENT '备注',
  `CREATE_TIME` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `CREATE_USER` varchar(20) NOT NULL COMMENT '创建人',
  `UPDATE_TIME` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  `UPDATE_USER` varchar(20) NOT NULL COMMENT '修改人',
  PRIMARY KEY (`ID`),
  KEY `idx_emp_no` (`EMP_NO`),
  KEY `idx_skill_type` (`SKILL_TYPE`),
  KEY `idx_skill_name` (`SKILL_NAME`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='员工个人特长表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_HX_EMP_SPECIAL_SKILL`
--

/*!40000 ALTER TABLE `T_HX_EMP_SPECIAL_SKILL` DISABLE KEYS */;
INSERT INTO `T_HX_EMP_SPECIAL_SKILL` VALUES (1,'EMP001','张伟','01','钢琴演奏','专业八级','中央音乐学院','从小学习钢琴','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(2,'EMP001','张伟','02','围棋','业余五段','中国围棋协会','公司围棋比赛冠军','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(3,'EMP002','王芳','03','英语','专业八级','教育部考试中心','可做专业翻译','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(4,'EMP006','杨光','04','摄影','高级摄影师','中国摄影家协会','擅长人像摄影','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(5,'EMP010','郑浩','05','网络安全','CISSP认证','国际信息系统安全协会','公司安全专家','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(6,'EMP003','李娜','01','小提琴','专业六级','上海音乐学院','曾获市级比赛奖项','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(7,'EMP007','赵敏','06','日语','N1级','日本国际交流基金会','商务日语流利','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(8,'EMP007','赵敏','07','项目管理','PMP认证','美国项目管理协会','擅长敏捷开发','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(9,'EMP004','刘强','08','篮球','国家二级运动员','广东省体育局','公司篮球队队长','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(10,'EMP019','曹阳','09','足球','国家三级运动员','广州市足协','司职前锋','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(11,'EMP005','陈静','10','UI设计','Adobe认证专家','Adobe公司','擅长交互设计','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(12,'EMP020','邓辉','11','插画','无级别',NULL,'业余插画师','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(13,'EMP008','周杰','12','软件测试','ISTQB认证','国际软件测试认证委员会','自动化测试专家','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(14,'EMP008','周杰','13','川菜烹饪','中级厨师','四川省烹饪协会','擅长川菜制作','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(15,'EMP009','吴婷','14','数据分析','CDA Level III','中国大数据产业联盟','擅长Python数据分析','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(16,'EMP016','高洁','15','演讲','无级别',NULL,'公司年会主持人','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(17,'EMP011','孙丽','16','法语','DELF B2','法国教育部','商务法语流利','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(18,'EMP014','林峰','17','书法','无级别',NULL,'楷书、行书','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(19,'EMP017','马超','18','云计算','AWS认证专家','亚马逊AWS','云架构设计','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin'),(20,'EMP018','黄蓉','19','茶艺','高级茶艺师','中国茶叶学会','精通茶道','2025-05-12 19:23:09','admin','2025-05-12 19:23:09','admin');
/*!40000 ALTER TABLE `T_HX_EMP_SPECIAL_SKILL` ENABLE KEYS */;

--
-- Table structure for table `t_hx_join_activity`
--

DROP TABLE IF EXISTS `t_hx_join_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_hx_join_activity` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `emp_no` varchar(20) NOT NULL COMMENT '员工档案号',
  `emp_name` varchar(50) NOT NULL COMMENT '员工姓名',
  `activity_type` varchar(3) DEFAULT NULL COMMENT '活动类型',
  `activity_name` varchar(100) DEFAULT NULL COMMENT '活动/项目/特长名称',
  `activity_group` varchar(3) DEFAULT NULL COMMENT '活动分类',
  `activity_level` varchar(3) DEFAULT NULL COMMENT '活动星级',
  `sponsor` varchar(100) DEFAULT NULL COMMENT '主办单位名称',
  `sponsor_level` varchar(30) NOT NULL COMMENT '主办单位级别',
  `activity_start_time` datetime NOT NULL COMMENT '举办时间起',
  `activity_end_time` datetime NOT NULL COMMENT '举办时间止',
  `is_reword` varchar(3) NOT NULL COMMENT '是否获奖(1是/0否)',
  `reword_level` varchar(30) NOT NULL COMMENT '表彰奖励类别',
  `reword_desc` varchar(300) NOT NULL COMMENT '获奖情况',
  `perform_desc` varchar(300) DEFAULT NULL COMMENT '表现评价',
  `perform_org` varchar(100) NOT NULL COMMENT '评价单位',
  `bz` varchar(300) DEFAULT NULL COMMENT '备注',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_user` varchar(20) NOT NULL COMMENT '创建人',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `update_user` varchar(20) NOT NULL COMMENT '更新人',
  PRIMARY KEY (`id`),
  KEY `idx_emp_no` (`emp_no`),
  KEY `idx_activity_type` (`activity_type`),
  KEY `idx_activity_name` (`activity_name`),
  KEY `idx_activity_time` (`activity_start_time`,`activity_end_time`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='员工参与活动记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_hx_join_activity`
--

/*!40000 ALTER TABLE `t_hx_join_activity` DISABLE KEYS */;
INSERT INTO `t_hx_join_activity` VALUES (1,'EMP001','张伟','01','全国企业艺术节','01','4','中国企业文化促进会','国家级','2023-06-15 14:00:00','2023-06-15 17:00:00','1','金奖','钢琴独奏《黄河》获表演类金奖','演奏技巧精湛，情感表达丰富','艺术节评委会',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(2,'EMP002','王芳','02','亚太区商业领袖论坛','03','5','世界经济论坛','国际级','2023-09-08 09:00:00','2023-09-10 18:00:00','0','无','担任主会场同声传译','翻译准确流畅，专业素养高','论坛组委会',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(3,'EMP003','李娜','01','上海国际艺术周','01','4','上海市文化局','省级','2023-11-20 19:30:00','2023-11-20 21:30:00','1','优秀表演奖','弦乐四重奏演出','音乐表现力强，团队配合默契','艺术周评委会',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(4,'EMP004','刘强','03','全国企业篮球联赛','02','3','中国企业体育协会','国家级','2023-07-22 10:00:00','2023-07-25 16:00:00','1','季军','作为主力队员带队获得第三名','场均得分18.5分，MVP候选人','赛事组委会',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(5,'EMP005','陈静','04','全国UI设计大赛','04','3','中国工业设计协会','国家级','2023-08-01 00:00:00','2023-08-31 23:59:59','1','银奖','企业级管理系统界面设计','创新性强，用户体验优化突出','大赛评委会',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(6,'EMP006','杨光','05','企业风采摄影展','01','2','集团工会','企业级','2023-05-04 09:00:00','2023-05-06 17:00:00','1','一等奖','组照《奋斗者》获一等奖','真实记录员工工作场景，富有感染力','评委会',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(7,'EMP007','赵敏','06','中日技术合作交流会','03','4','日本贸易振兴机构','国际级','2023-10-12 13:00:00','2023-10-13 17:00:00','0','无','担任技术洽谈首席翻译','专业术语准确，促进双方深入交流','项目组',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(8,'EMP008','周杰','07','成都国际美食节','05','3','成都市商务局','省级','2023-12-08 10:00:00','2023-12-10 20:00:00','1','最佳创意奖','川菜创新菜品展示','传统与创新结合，获得观众好评','美食节组委会',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(9,'EMP009','吴婷','08','全国大数据分析挑战赛','04','4','中国计算机学会','国家级','2023-04-15 00:00:00','2023-04-17 23:59:59','1','冠军','金融风控模型分析第一名','算法创新，预测准确率领先','竞赛委员会',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(10,'EMP010','郑浩','09','国家网络安全攻防演练','06','5','中央网信办','国家级','2023-03-01 09:00:00','2023-03-03 18:00:00','1','优秀防守团队','成功防御所有攻击','安全策略完善，应急响应迅速','演练指挥部',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(11,'EMP011','孙丽','02','中法数字经济论坛','03','4','法国驻华使馆','国际级','2023-06-28 08:30:00','2023-06-29 17:00:00','0','无','负责法方嘉宾接待','沟通顺畅，服务周到','论坛秘书处',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(12,'EMP014','林峰','01','传统文化传承展','01','3','中国文联','国家级','2023-09-15 10:00:00','2023-09-17 16:00:00','1','传承奖','现场书法表演','楷书作品被主办方收藏','活动组委会',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(13,'EMP017','马超','08','全球云计算峰会','04','5','国际云计算协会','国际级','2023-07-10 09:00:00','2023-07-12 18:00:00','0','无','发表《混合云架构实践》主题演讲','内容专业，现场反响热烈','峰会组委会',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(14,'EMP018','黄蓉','10','国际茶文化节','05','4','中国茶叶流通协会','国家级','2023-04-20 09:00:00','2023-04-22 17:00:00','1','最佳表演奖','宋代点茶技艺展示','完整还原传统工艺，文化内涵丰富','评委会',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(15,'EMP019','曹阳','03','粤港澳大湾区足球赛','02','3','广东省体育局','省级','2023-08-12 14:00:00','2023-08-15 20:00:00','1','最佳射手','个人进球6个','跑位灵活，射门精准','赛事组委会',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(16,'EMP020','邓辉','01','当代青年艺术展','01','3','中国美术家协会','国家级','2023-12-01 10:00:00','2023-12-07 18:00:00','1','新锐奖','系列插画《城市记忆》','风格独特，引发观众共鸣','展览评委会',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(17,'EMP001','张伟','03','全国职工围棋锦标赛','02','4','中华全国总工会','国家级','2023-05-20 09:00:00','2023-05-22 17:00:00','1','八强','个人赛进入前八名','棋风稳健，计算精准','赛事组委会',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(18,'EMP007','赵敏','11','敏捷开发研讨会','07','2','集团技术中心','企业级','2023-11-15 13:30:00','2023-11-15 17:00:00','0','无','担任活动总协调人','流程顺畅，参会满意度95%','人力资源部',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(19,'EMP009','吴婷','12','数据分析师内训','07','2','集团培训中心','企业级','2023-02-10 09:00:00','2023-02-11 17:00:00','0','无','主讲《Python数据分析实战》','课程评分4.8/5.0','培训评估小组',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin'),(20,'EMP010','郑浩','12','网络安全意识公开课','07','3','市网络安全协会','市级','2023-09-28 14:00:00','2023-09-28 16:30:00','0','无','主讲《企业数据安全防护》','案例生动，实用性强','协会秘书处',NULL,'2025-05-12 19:24:17','admin','2025-05-12 19:24:17','admin');
/*!40000 ALTER TABLE `t_hx_join_activity` ENABLE KEYS */;

--
-- Table structure for table `t_hx_parttime_job`
--

DROP TABLE IF EXISTS `t_hx_parttime_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_hx_parttime_job` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `emp_no` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '员工档案号',
  `emp_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '员工姓名',
  `parttime_job` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '兼职岗位',
  `parttime_address` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '兼职单位',
  `parttime_time` datetime DEFAULT NULL COMMENT '兼职时间',
  `bz` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_user` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '创建人',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `update_user` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '更新人',
  PRIMARY KEY (`id`),
  KEY `idx_emp_no` (`emp_no`),
  KEY `idx_parttime_job` (`parttime_job`),
  KEY `idx_parttime_address` (`parttime_address`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='员工岗位兼职记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_hx_parttime_job`
--

/*!40000 ALTER TABLE `t_hx_parttime_job` DISABLE KEYS */;
INSERT INTO `t_hx_parttime_job` VALUES (1,'EMP001','张伟','艺术指导','星辰文化传媒有限公司','2023-07-01 00:00:00','负责企业文艺活动策划','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(2,'EMP002','王芳','外语培训讲师','环球语言培训中心','2023-10-15 00:00:00','周末商务英语课程讲师','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(3,'EMP003','李娜','乐团客座演奏员','上海爱乐乐团','2023-12-01 00:00:00','定期参与乐团排练演出','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(4,'EMP004','刘强','青少年篮球教练','飞跃体育培训学校','2023-08-01 00:00:00','周末青少年篮球培训','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(5,'EMP005','陈静','UI设计顾问','创想数字科技有限公司','2023-09-01 00:00:00','每月提供2次设计指导','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(6,'EMP006','杨光','特约摄影师','视觉中国图库','2023-06-01 00:00:00','商业图库供稿摄影师','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(7,'EMP007','赵敏','会议同传译员','全球会议服务公司','2023-11-01 00:00:00','按项目承接翻译工作','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(8,'EMP008','周杰','美食专栏作家','美味生活杂志社','2024-01-01 00:00:00','每月撰写2篇美食文章','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(9,'EMP009','吴婷','数据分析导师','数据科学研习社','2023-05-01 00:00:00','线上数据分析课程讲师','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(10,'EMP010','郑浩','安全技术顾问','网络安全联盟','2023-04-01 00:00:00','提供企业安全评估服务','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(11,'EMP011','孙丽','法语家教','精英外语教育','2023-07-15 00:00:00','周末一对一法语教学','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(12,'EMP014','林峰','书法培训班讲师','传统文化书院','2023-10-01 00:00:00','每周三晚书法课程','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(13,'EMP017','马超','云技术布道师','云计算开发者社区','2023-08-15 00:00:00','技术文章撰写与分享','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(14,'EMP018','黄蓉','茶文化讲师','禅意茶生活馆','2023-05-10 00:00:00','每月举办2次茶艺讲座','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(15,'EMP019','曹阳','足球解说员','体育直播平台','2023-09-15 00:00:00','业余足球赛事解说','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(16,'EMP020','邓辉','自由插画师','插画师联盟','2023-12-15 00:00:00','承接商业插画项目','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(17,'EMP001','张伟','围棋启蒙老师','黑白围棋教室','2023-06-01 00:00:00','周末儿童围棋教学','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(18,'EMP007','赵敏','项目管理培训师','职业发展学院','2023-12-01 00:00:00','每月1次项目管理培训','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(19,'EMP009','吴婷','数据竞赛评委','全国大学生数据竞赛组委会','2023-03-01 00:00:00','季度性竞赛评审工作','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin'),(20,'EMP010','郑浩','安全技术专栏作者','网络安全前沿杂志','2023-02-01 00:00:00','每月撰写安全技术文章','2025-05-12 19:24:58','admin','2025-05-12 19:24:58','admin');
/*!40000 ALTER TABLE `t_hx_parttime_job` ENABLE KEYS */;

--
-- Table structure for table `t_hx_test_evaluate`
--

DROP TABLE IF EXISTS `t_hx_test_evaluate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_hx_test_evaluate` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `evaluate_type` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '考察类型',
  `emp_no` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '被考察人档案号',
  `emp_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '被考察人姓名',
  `evaluate_time` datetime DEFAULT NULL COMMENT '考察时间',
  `evaluate_suggest` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '考评建议',
  `evaluate_result` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '考评结果',
  `super_evaluate` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '上级评价',
  `lever_evaluate` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '平级评价',
  `emp_evaluate` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '员工评价',
  `evaluate_emp_no` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '考察人员档案号',
  `evaluate_emp_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '考察人员姓名',
  `other_msg` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '其他信息',
  `remark` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `create_user` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '创建人',
  `update_user` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '更新人',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_emp_no` (`emp_no`),
  KEY `idx_evaluate_time` (`evaluate_time`),
  KEY `idx_evaluate_emp` (`evaluate_emp_no`),
  KEY `idx_evaluate_type` (`evaluate_type`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='员工考察考评表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_hx_test_evaluate`
--

/*!40000 ALTER TABLE `t_hx_test_evaluate` DISABLE KEYS */;
INSERT INTO `t_hx_test_evaluate` VALUES (1,'01','EMP001','张伟','2023-12-10 14:00:00','建议加强跨部门协作能力','良好','艺术修养深厚，工作有创意，但进度把控需加强','乐于分享专业知识，团队合作意识强','我认为在项目创新方面表现突出','MGR001','李总监',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(2,'02','EMP002','王芳','2023-11-15 09:30:00','具备管理潜质，建议晋升','优秀','语言能力突出，国际项目表现优异，具备领导力','沟通协调能力强，乐于助人','希望承担更多国际项目管理工作','MGR002','王总监',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(3,'03','EMP003','李娜','2023-10-20 10:00:00','建议将艺术专长更多融入工作','良好','专业技能扎实，但工作创新性不足','艺术气质突出，团队活动积极参与','希望公司支持员工艺术发展','MGR003','张经理',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(4,'04','EMP004','刘强','2023-09-05 15:00:00','建议提升文档撰写能力','合格','执行力强，但工作文档质量需提高','团队精神突出，体育活动组织能力强','我会加强业务文档写作训练','MGR004','赵经理',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(5,'01','EMP005','陈静','2023-12-12 11:00:00','建议加强设计规范宣导','优秀','设计能力专业，多次获得客户好评','设计风格独特，乐于分享经验','希望建立公司统一设计规范','MGR005','陈总监',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(6,'05','EMP006','杨光','2023-08-18 14:30:00','建议加强技术深度','合格','工作态度端正，但专业技术需提升','团队活动积极参与，摄影作品优秀','我会加强专业技术学习','MGR006','周经理',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(7,'01','EMP007','赵敏','2023-12-05 10:00:00','建议培养更多语言人才','优秀','国际项目核心成员，语言能力突出','跨文化沟通桥梁，团队不可或缺','愿意培养新人语言能力','MGR007','吴总监',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(8,'03','EMP008','周杰','2023-09-22 13:00:00','建议将美食专长用于团队建设','良好','工作认真负责，创新能力突出','团队聚餐活跃分子，厨艺精湛','可以组织更多美食团建活动','MGR008','郑经理',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(9,'02','EMP009','吴婷','2023-11-20 09:00:00','建议组建数据分析团队','优秀','数据分析能力顶尖，具备团队管理潜力','技术分享积极，带动团队进步','希望带领数据分析团队','MGR009','钱总监',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(10,'01','EMP010','郑浩','2023-12-08 15:30:00','建议加强安全意识培训','优秀','安全技术专家，多次防范重大风险','技术问题解决能力强，乐于助人','愿意开展全员安全培训','MGR010','孙总监',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(11,'04','EMP011','孙丽','2023-10-15 10:30:00','建议提升项目推进效率','良好','语言能力优秀，但项目跟进需更主动','文化氛围营造者，团队开心果','会改进项目跟进方式','MGR001','李总监',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(12,'01','EMP014','林峰','2023-12-15 14:00:00','建议将传统文化融入设计','良好','工作踏实稳重，传统文化底蕴深厚','团队活动积极参与，书法作品受欢迎','希望将传统美学融入现代设计','MGR003','张经理',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(13,'02','EMP017','马超','2023-11-25 09:00:00','建议负责云技术团队','优秀','云计算技术专家，演讲能力突出','技术分享内容丰富，带动团队学习','愿意带领云技术团队','MGR005','陈总监',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(14,'03','EMP018','黄蓉','2023-09-28 13:30:00','建议组织茶艺文化活动','良好','工作细致认真，茶艺专长突出','客户接待表现优异，文化素养高','可以组织茶艺客户活动','MGR007','吴总监',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(15,'04','EMP019','曹阳','2023-08-30 15:00:00','建议提升文档规范','合格','工作热情高，但文档规范性不足','体育活动组织核心，团队精神好','会加强文档规范学习','MGR009','钱总监',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(16,'01','EMP020','邓辉','2023-12-18 11:00:00','建议参与公司视觉设计','优秀','创意能力突出，多次解决设计难题','艺术感觉敏锐，设计作品受欢迎','愿意参与公司品牌视觉设计','MGR002','王总监',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(17,'03','EMP001','张伟','2023-07-20 10:00:00','建议组织棋类团建活动','良好','逻辑思维能力强，围棋教学受欢迎','团队智力活动组织者，凝聚力强','可以组织棋类团建活动','MGR004','赵经理',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(18,'01','EMP007','赵敏','2023-12-20 09:30:00','建议负责国际项目管理培训','优秀','国际项目核心管理者，培训能力突出','项目管理经验丰富，乐于分享','愿意建立国际项目管理培训体系','MGR006','周经理',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(19,'03','EMP009','吴婷','2023-06-15 14:00:00','建议主导数据人才选拔','优秀','数据技术权威，评审公正专业','技术判断准确，培养新人用心','愿意参与数据人才选拔体系','MGR008','郑经理',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40'),(20,'01','EMP010','郑浩','2023-12-22 15:00:00','建议建立安全技术知识库','优秀','安全技术领袖，文章影响力大','技术传播者，提升团队安全水平','愿意构建安全技术知识体系','MGR010','孙总监',NULL,NULL,'admin','admin','2025-05-12 19:25:40','2025-05-12 19:25:40');
/*!40000 ALTER TABLE `t_hx_test_evaluate` ENABLE KEYS */;

--
-- Dumping routines for database 'talent_engine'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-28 15:59:55
