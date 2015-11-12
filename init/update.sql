CREATE TABLE `ops_menu` (
  `mid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '菜单ID',
  `preid` int(11) NOT NULL DEFAULT '0' COMMENT '上级节点ID，默认0-TOP',
  `name` varchar(32) NOT NULL COMMENT '菜单名称',
  `keys` varchar(32) NOT NULL DEFAULT '' COMMENT '菜单KEYS',
  `url` varchar(128) NOT NULL DEFAULT '' COMMENT 'URL名称',
  `is_func` tinyint(3) NOT NULL DEFAULT '1' COMMENT '是否功能页面（0-否；1-是）',
  `level` tinyint(4) NOT NULL DEFAULT '1' COMMENT '菜单层级',
  `status` tinyint(3) NOT NULL DEFAULT '1' COMMENT '启用状态：0-不启用（默认）；1-启用',
  `dml_flag` tinyint(4) NOT NULL DEFAULT '1' COMMENT '操作标识：1：新增；2：更新；3：删除。',
  `dml_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据最后修改时间',
  PRIMARY KEY (`mid`),
  KEY `pre_key` (`preid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系统菜单表';

INSERT INTO `ops_menu` VALUES (1, 0, '域名管理', 'DomainManager', '#', 1, 1, 1, 1, '2015-10-28 00:18:35'),
  (2, 0, 'MySQL', 'MySQL', '#', 1, 1, 1, 1, '2015-10-28 00:18:28'),
  (3, 1, '域名列表', 'DomainList', '/domain/', 1, 2, 1, 1, '2015-10-28 19:59:24'),
  (4, 2, 'Query-Digest-UI', 'Digest', '/digest/', 1, 2, 1, 1, '2015-10-28 20:01:05'),
  (5, 2, 'Redis', 'Redis', '/redis/', 1, 2, 1, 1, '2015-10-28 20:01:02'),
  (6, 0, 'Admin设置', 'AdminSet', '#', 1, 1, 1, 1, '2015-11-02 02:10:27'),
  (7, 6, '用户权限', 'UserPrivilege', '/privilege/', 1, 2, 1, 1, '2015-11-02 02:12:04'),
  (8, 1, '运营域名列表', 'OpDomainList', '/op/domain/', 1, 2, 1, 1, '2015-11-10 19:04:33');

CREATE TABLE `ops_priv_data` (
  `uid` int(10) unsigned NOT NULL COMMENT '用户ID',
  `mid` int(10) unsigned NOT NULL COMMENT '菜单ID',
  `pid` int(10) unsigned NOT NULL COMMENT '项目ID',
  `r_priv` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '读权限',
  `w_priv` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '写权限',
  `dml_flag` tinyint(4) NOT NULL DEFAULT '1' COMMENT '操作标识：1：新增；2：更新；3：删除。',
  `dml_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据最后修改时间',
  PRIMARY KEY (`uid`,`mid`,`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='数据菜单权限信息表';


CREATE TABLE `redis_info` (
  `redis_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Redis ID',
  `project_id` int(11) DEFAULT NULL COMMENT '项目ID',
  `project_name` varchar(64) DEFAULT NULL COMMENT '项目名称',
  `command` varchar(256) DEFAULT NULL COMMENT 'Redis 执行命令',
  `status` int(11) DEFAULT NULL COMMENT 'Redis 执行结果状态',
  `redis_file_path` varchar(256) DEFAULT NULL COMMENT 'Redis下载路径',
  `redis_filename` varchar(256) DEFAULT NULL COMMENT 'Redis下载文件名',
  `apply_user_id` int(11) DEFAULT NULL COMMENT 'Redis申请人',
  `init_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据创建时间',
  `dml_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据最后修改时间',
  `dml_flag` tinyint(4) NOT NULL DEFAULT '1' COMMENT '数据操作标识: 1-新增;2-修改;3-删除',
  PRIMARY KEY (`redis_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COMMENT='Redis信息表';


CREATE TABLE `system_datadict` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增长ID',
  `pre_id` int(11) NOT NULL COMMENT '父ID',
  `name` varchar(64) NOT NULL COMMENT '名称',
  `init_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据创建时间',
  `dml_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据最后修改时间',
  `dml_flag` tinyint(4) NOT NULL DEFAULT '1' COMMENT '数据操作标识: 1-新增;2-修改;3-删除',
  `value` varchar(64) DEFAULT NULL COMMENT '对应值',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='系统字典表';

INSERT INTO `system_datadict` VALUES (1, 0, '执行状态', '2015-10-22 16:21:00', '2015-10-22 01:30:40', 1, '0'),
  (2, 1, '成功', '2015-10-22 16:21:00', '2015-10-22 01:28:29', 1, '1'),
  (3, 1, '失败', '2015-10-22 16:21:00', '2015-10-22 01:28:31', 1, '2');

INSERT INTO `project` VALUES (1,'V项目','video',NULL,NULL),(2,'论坛','discuze',NULL,NULL);

alter table `domain_info` add `op_comments` varchar(255) DEFAULT NULL COMMENT '运营备注';
alter table `project` add `project_keys` varchar(32) DEFAULT NULL COMMENT '项目keys';
