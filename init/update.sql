
CREATE TABLE `domain_info` (
  `domain_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '域名ID',
  `domain_name` varchar(64) NOT NULL COMMENT '主域名',
  `project_id` int(11) DEFAULT NULL COMMENT '项目ID',
  `project_name` varchar(64) DEFAULT NULL COMMENT '项目名称',
  `ip_source` varchar(16) DEFAULT NULL COMMENT '源IP',
  `status` enum('已解析','未解析') DEFAULT NULL COMMENT '域名状态',
  `cdn_hightanti` varchar(64) DEFAULT NULL COMMENT '解析是CDN or 高防',
  `pre_domain_id` int(11) NOT NULL DEFAULT '0' COMMENT '父域ID，顶级域名为0',
  `functions` varchar(255) DEFAULT NULL COMMENT '用途',
  `comments` varchar(255) DEFAULT NULL COMMENT '备注',
  `is_public` int(11) NOT NULL DEFAULT '0' COMMENT '开放给运营',
  `register` varchar(64) DEFAULT NULL COMMENT '注册商',
  `register_date` datetime DEFAULT NULL COMMENT '注册时间',
  `domain_DNS` varchar(64) DEFAULT NULL COMMENT '域名解析',
  `expiration` date DEFAULT NULL COMMENT '过期时间',
  `init_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据创建时间',
  `dml_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据最后修改时间',
  `dml_flag` tinyint(4) NOT NULL DEFAULT '1' COMMENT '数据操作标识: 1-新增;2-修改;3-删除',
  PRIMARY KEY (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='域名信息表';


CREATE TABLE `ops_menu` (
  `mid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '菜单ID',
  `preid` int(11) NOT NULL DEFAULT '0' COMMENT '上级节点ID，默认0-TOP',
  `name` varchar(32) NOT NULL COMMENT '菜单名称',
  `url` varchar(128) NOT NULL DEFAULT '' COMMENT 'URL名称',
  `is_func` tinyint(3) NOT NULL DEFAULT '1' COMMENT '是否功能页面（0-否；1-是）',
  `level` tinyint(4) NOT NULL DEFAULT '1' COMMENT '菜单层级',
  `status` tinyint(3) NOT NULL DEFAULT '1' COMMENT '启用状态：0-不启用（默认）；1-启用',
  `dml_flag` tinyint(4) NOT NULL DEFAULT '1' COMMENT '操作标识：1：新增；2：更新；3：删除。',
  `dml_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据最后修改时间',
  PRIMARY KEY (`mid`),
  KEY `pre_key` (`preid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COMMENT='系统菜单表';


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
