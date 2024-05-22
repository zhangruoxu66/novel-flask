SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for admin_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `admin_admin_log`;
CREATE TABLE `admin_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `method` varchar(10) DEFAULT NULL,
  `uid` int DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `desc` text,
  `ip` varchar(255) DEFAULT NULL,
  `success` int DEFAULT NULL,
  `user_agent` text,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of admin_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for admin_dept
-- ----------------------------
DROP TABLE IF EXISTS `admin_dept`;
CREATE TABLE `admin_dept` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '部门ID',
  `parent_id` int DEFAULT NULL COMMENT '父级编号',
  `dept_name` varchar(50) DEFAULT NULL COMMENT '部门名称',
  `sort` int DEFAULT NULL COMMENT '排序',
  `leader` varchar(50) DEFAULT NULL COMMENT '负责人',
  `phone` varchar(20) DEFAULT NULL COMMENT '联系方式',
  `email` varchar(50) DEFAULT NULL COMMENT '邮箱',
  `status` int DEFAULT NULL COMMENT '状态(1开启,0关闭)',
  `remark` text COMMENT '备注',
  `address` varchar(255) DEFAULT NULL COMMENT '详细地址',
  `create_at` datetime DEFAULT NULL COMMENT '创建时间',
  `update_at` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of admin_dept
-- ----------------------------
INSERT INTO `admin_dept` VALUES ('1', '0', '总公司', '1', '就眠仪式', '12312345679', '123qq.com', '1', '这是总公司', null, '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dept` VALUES ('4', '1', '济南分公司', '2', '就眠仪式', '12312345679', '123qq.com', '1', '这是济南', null, '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dept` VALUES ('5', '1', '唐山分公司', '4', 'mkg', '12312345679', '123qq.com', '1', '这是唐山', null, '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dept` VALUES ('7', '4', '济南分公司开发部', '5', '就眠仪式', '12312345679', '123qq.com', '1', '测试', null, '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dept` VALUES ('8', '5', '唐山测试部', '5', 'mkg', '12312345679', '123qq.com', '1', '测试部', null, '2023-04-30 18:00:00', '2023-04-30 18:00:00');

-- ----------------------------
-- Table structure for admin_dict_data
-- ----------------------------
DROP TABLE IF EXISTS `admin_dict_data`;
CREATE TABLE `admin_dict_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data_label` varchar(255) DEFAULT NULL COMMENT '字典类型名称',
  `data_value` varchar(255) DEFAULT NULL COMMENT '字典类型标识',
  `type_code` varchar(255) DEFAULT NULL COMMENT '字典类型描述',
  `is_default` int DEFAULT '0' COMMENT '是否默认',
  `enable` int DEFAULT NULL COMMENT '是否开启',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '' COMMENT '备注',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of admin_dict_data
-- ----------------------------
INSERT INTO `admin_dict_data` VALUES ('1', '是', '1', 'YES_OR_NO', '0', '1', ' ', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('2', '否', '0', 'YES_OR_NO', '0', '1', ' ', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('3', '男', '0', 'SEX', '0', '1', ' ', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('4', '女', '1', 'SEX', '0', '1', ' ', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('5', '轮播图', '0', 'book_rec_type', '0', '1', '轮播图', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('6', '顶部小说栏', '1', 'book_rec_type', '0', '1', '顶部小说栏', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('7', '本周强推', '2', 'book_rec_type', '0', '1', '本周强推', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('8', '热门推荐', '3', 'book_rec_type', '0', '1', '热门推荐', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('9', '精品推荐', '4', 'book_rec_type', '0', '1', '精品推荐', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('10', '男频', '0', 'work_direction', '0', '1', '男频', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('11', '女频', '1', 'work_direction', '0', '1', '女频', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('12', '连载中', '0', 'book_status', '0', '1', '连载中', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('13', '已完结', '1', 'book_status', '0', '1', '已完结', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('14', '免费', '0', 'book_is_vip', '0', '1', '免费', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('15', '收费', '1', 'book_is_vip', '0', '1', '收费', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('16', '默认排序', '0', 'book_order_by_type', '0', '1', '默认排序（id降序）', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('17', '添加时间', '1', 'book_order_by_type', '0', '1', '添加时间降序', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('18', '按最新更新时间排序', '2', 'book_order_by_type', '0', '1', '按最新更新时间降序排序', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('19', '按点击量排序', '3', 'book_order_by_type', '0', '1', '按点击量降序排序', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('20', '按字数排序', '4', 'book_order_by_type', '0', '1', '按字数降序排序', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('21', '按评论数量排序', '5', 'book_order_by_type', '0', '1', '按评论数量降序排序', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('22', '按昨日订阅数排序', '6', 'book_order_by_type', '0', '1', '按昨日订阅数降序排序', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('23', '禁用', '0', 'is_enable', '0', '1', '禁用', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('24', '启用', '1', 'is_enable', '0', '1', '启用', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('25', '待审核', '0', 'audit_status', '0', '1', '待审核', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('26', '审核通过', '1', 'audit_status', '0', '1', '审核通过', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('27', '审核不通过', '2', 'audit_status', '0', '1', '审核不通过', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('28', '充值失败', '0', 'pay_status', '0', '1', '充值失败', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('29', '充值成功', '1', 'pay_status', '0', '1', '充值成功', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('30', '待支付', '2', 'pay_status', '0', '1', '待支付', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('31', '正常', '0', 'author_status', '0', '1', '正常', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('32', '冻结', '1', 'author_status', '0', '1', '冻结', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('33', '下架', '0', 'on_off_status', '0', '1', '下架', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_data` VALUES ('34', '上架', '1', 'on_off_status', '0', '1', '上架', '2023-04-30 18:00:00', '2023-04-30 18:00:00');

-- ----------------------------
-- Table structure for admin_dict_type
-- ----------------------------
DROP TABLE IF EXISTS `admin_dict_type`;
CREATE TABLE `admin_dict_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type_name` varchar(255) DEFAULT NULL COMMENT '字典类型名称',
  `type_code` varchar(255) DEFAULT NULL COMMENT '字典类型标识',
  `description` varchar(255) DEFAULT NULL COMMENT '字典类型描述',
  `enable` int DEFAULT NULL COMMENT '是否开启',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of admin_dict_type
-- ----------------------------
INSERT INTO `admin_dict_type` VALUES ('1', '是否', 'YES_OR_NO', '1是0否，默认0', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_type` VALUES ('2', '性别', 'SEX', '0男1女', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_type` VALUES ('3', '小说推荐类型', 'book_rec_type', '小说推荐类型', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_type` VALUES ('4', '作品方向', 'work_direction', '作品方向', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_type` VALUES ('5', '小说状态', 'book_status', '小说状态', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_type` VALUES ('6', '是否收费', 'book_is_vip', '是否收费', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_type` VALUES ('7', '小说排序方式', 'book_order_by_type', '小说排序方式', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_type` VALUES ('8', '是否启用', 'is_enable', '是否启用（启用状态）', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_type` VALUES ('9', '评论审核状态', 'audit_status', '评论审核状态', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_type` VALUES ('10', '支付状态', 'pay_status', '支付状态', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_type` VALUES ('11', '作家状态', 'author_status', '作家状态', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_dict_type` VALUES ('12', '小说在架状态', 'on_off_status', '小说在架状态', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00');

-- ----------------------------
-- Table structure for admin_mail
-- ----------------------------
DROP TABLE IF EXISTS `admin_mail`;
CREATE TABLE `admin_mail` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '邮件编号',
  `receiver` varchar(1024) DEFAULT NULL COMMENT '收件人邮箱',
  `subject` varchar(128) DEFAULT NULL COMMENT '邮件主题',
  `content` text COMMENT '邮件正文',
  `user_id` int DEFAULT NULL COMMENT '发送人id',
  `create_at` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of admin_mail
-- ----------------------------

-- ----------------------------
-- Table structure for admin_photo
-- ----------------------------
DROP TABLE IF EXISTS `admin_photo`;
CREATE TABLE `admin_photo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `href` varchar(255) DEFAULT NULL,
  `mime` char(50) NOT NULL,
  `size` char(30) NOT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of admin_photo
-- ----------------------------

-- ----------------------------
-- Table structure for admin_power
-- ----------------------------
DROP TABLE IF EXISTS `admin_power`;
CREATE TABLE `admin_power` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '权限编号',
  `name` varchar(255) DEFAULT NULL COMMENT '权限名称',
  `type` varchar(1) DEFAULT NULL COMMENT '权限类型',
  `code` varchar(30) DEFAULT NULL COMMENT '权限标识',
  `url` varchar(255) DEFAULT NULL COMMENT '权限路径',
  `open_type` varchar(10) DEFAULT NULL COMMENT '打开方式',
  `parent_id` int DEFAULT NULL COMMENT '父类编号',
  `icon` varchar(128) DEFAULT NULL COMMENT '图标',
  `sort` int DEFAULT NULL COMMENT '排序',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `enable` int DEFAULT NULL COMMENT '是否开启',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of admin_power
-- ----------------------------
INSERT INTO `admin_power` VALUES ('1', '系统管理', '0', '', null, null, '0', 'layui-icon layui-icon-set-fill', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('3', '用户管理', '1', 'admin:user:main', '/admin/user/', '_iframe', '1', 'layui-icon layui-icon layui-icon layui-icon layui-icon-rate', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('4', '权限管理', '1', 'admin:power:main', '/admin/power/', '_iframe', '1', null, '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('9', '角色管理', '1', 'admin:role:main', '/admin/role', '_iframe', '1', 'layui-icon layui-icon-username', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('12', '系统监控', '1', 'admin:monitor:main', '/admin/monitor', '_iframe', '1', 'layui-icon layui-icon-vercode', '5', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('13', '日志管理', '1', 'admin:log:main', '/admin/log', '_iframe', '1', 'layui-icon layui-icon-read', '4', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('17', '文件管理', '0', null, null, null, '0', 'layui-icon layui-icon-picture', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('18', '图片上传', '1', 'admin:file:main', '/admin/file', '_iframe', '17', 'layui-icon layui-icon-camera', '5', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('21', '权限增加', '2', 'admin:power:add', '', '', '4', 'layui-icon layui-icon-add-circle', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('22', '用户增加', '2', 'admin:user:add', '', '', '3', 'layui-icon layui-icon-add-circle', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('23', '用户编辑', '2', 'admin:user:edit', '', '', '3', 'layui-icon layui-icon-rate', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('24', '用户删除', '2', 'admin:user:remove', '', '', '3', '', '3', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('25', '权限编辑', '2', 'admin:power:edit', '', '', '4', '', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('26', '用户删除', '2', 'admin:power:remove', '', '', '4', '', '3', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('27', '用户增加', '2', 'admin:role:add', '', '', '9', '', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('28', '角色编辑', '2', 'admin:role:edit', '', '', '9', '', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('29', '角色删除', '2', 'admin:role:remove', '', '', '9', '', '3', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('30', '角色授权', '2', 'admin:role:power', '', '', '9', '', '4', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('31', '图片增加', '2', 'admin:file:add', '', '', '18', '', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('32', '图片删除', '2', 'admin:file:delete', '', '', '18', '', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('44', '数据字典', '1', 'admin:dict:main', '/admin/dict', '_iframe', '1', 'layui-icon layui-icon-console', '6', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('45', '字典增加', '2', 'admin:dict:add', '', '', '44', '', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('46', '字典修改', '2', 'admin:dict:edit', '', '', '44', '', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('47', '字典删除', '2', 'admin:dict:remove', '', '', '44', '', '3', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('48', '部门管理', '1', 'admin:dept:main', '/dept', '_iframe', '1', 'layui-icon layui-icon-group', '3', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('49', '部门增加', '2', 'admin:dept:add', '', '', '48', '', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('50', '部门编辑', '2', 'admin:dept:edit', '', '', '48', '', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('51', '部门删除', '2', 'admin:dept:remove', '', '', '48', '', '3', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('52', '定时任务', '0', '', '', '', '0', 'layui-icon layui-icon-log', '3', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('53', '任务管理', '1', 'admin:task:main', '/admin/task', '_iframe', '52', 'layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('54', '任务增加', '2', 'admin:task:add', '', '', '53', 'layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('55', '任务修改', '2', 'admin:task:edit', '', '', '53', 'layui-icon ', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('56', '任务删除', '2', 'admin:task:remove', '', '', '53', 'layui-icon ', '23', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('57', '邮件管理', '1', 'admin:mail:main', '/admin/mail', '_iframe', '1', 'layui-icon ', '7', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('58', '邮件发送', '2', 'admin:mail:add', '', '', '57', 'layui-icon layui-icon-ok-circle', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('59', '邮件删除', '2', 'admin:mail:remove', '', '', '57', '', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('66', '会员管理', '0', null, null, null, '0', 'layui-icon layui-icon-username', '6', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('67', '会员列表', '1', 'admin:member:main', '/admin/member/', '_iframe', '66', 'layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('68', '会员反馈', '1', 'admin:member_feedback:main', '/admin/member_feedback', '_iframe', '66', 'layui-icon layui-icon layui-icon layui-icon ', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('69', '网站管理', '0', null, null, null, '0', 'layui-icon layui-icon-website', '4', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('70', '网站信息', '1', 'admin:website_info:main', '/admin/website_info/', '_iframe', '69', 'layui-icon layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('71', '修改网站信息', '2', 'admin:website_info:edit', null, null, '70', 'layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('72', '小说推荐', '1', 'admin:book_setting:main', '/admin/book_setting/', '_iframe', '69', 'layui-icon layui-icon layui-icon-read', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('73', '友情链接', '1', 'admin:friend_link:main', '/admin/friend_link/', '_iframe', '69', 'layui-icon ', '3', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('74', '新增', '2', 'admin:book_setting:add', null, null, '72', 'layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('75', '修改', '2', 'admin:book_setting:edit', null, null, '72', 'layui-icon ', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('76', '删除', '2', 'admin:book_setting:remove', null, null, '72', 'layui-icon layui-icon ', '3', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('77', '新增', '2', 'admin:friend_link:add', null, null, '73', 'layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('78', '修改', '2', 'admin:friend_link:edit', null, null, '73', 'layui-icon ', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('79', '删除', '2', 'admin:friend_link:remove', null, null, '73', 'layui-icon layui-icon ', '3', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('80', '小说管理', '0', null, null, null, '0', 'layui-icon layui-icon layui-icon-read', '8', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('81', '小说列表', '1', 'admin:book:main', '/admin/book/', '_iframe', '80', 'layui-icon layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('82', '评论管理', '1', 'admin:book_comment:main', '/admin/book_comment/', '_iframe', '80', 'layui-icon layui-icon layui-icon layui-icon ', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('83', '删除', '2', 'admin:book:remove', null, null, '81', 'layui-icon layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('84', '查看详情', '2', 'admin:book:detail', null, null, '81', 'layui-icon layui-icon ', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('85', '查看评论详情', '2', 'admin:book_comment:detail', null, null, '82', 'layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('86', '删除评论', '2', 'admin:book_comment:remove', null, null, '82', 'layui-icon ', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('87', '新闻管理', '0', null, null, null, '0', 'layui-icon layui-icon-login-weibo', '5', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('88', '类别管理', '1', 'admin:news_category:main', '/admin/news_category/', '_iframe', '87', 'layui-icon layui-icon layui-icon layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('89', '新闻列表', '1', 'admin:news:main', '/admin/news/', '_iframe', '87', 'layui-icon ', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('90', '新增类别', '2', 'admin:news_category:add', null, null, '88', 'layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('91', '删除类别', '2', 'admin:news_category:remove', null, null, '88', 'layui-icon ', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('92', '修改类别', '2', 'admin:news_category:edit', null, null, '88', 'layui-icon ', '3', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('93', '添加新闻', '2', 'admin:news:add', null, null, '89', 'layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('94', '删除新闻', '2', 'admin:news:remove', null, null, '89', 'layui-icon ', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('95', '修改新闻', '2', 'admin:news:edit', null, null, '89', 'layui-icon ', '3', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('96', '作家管理', '0', null, null, null, '0', 'layui-icon layui-icon-username', '7', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('97', '邀请码管理', '1', 'admin:invite_code:main', '/admin/invite_code/', '_iframe', '96', 'layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('98', '新增邀请码', '2', 'admin:invite_code:add', null, null, '97', 'layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('99', '删除邀请码', '2', 'admin:invite_code:remove', null, null, '97', 'layui-icon ', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('100', '作者列表', '1', 'admin:author:main', '/admin/author/', '_iframe', '96', 'layui-icon ', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('101', '封禁解封', '2', 'admin:author:enable_disable', null, null, '100', 'layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('102', '订单管理', '0', null, null, null, '0', 'layui-icon layui-icon layui-icon-rmb', '9', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('103', '订单列表', '1', 'admin:order:main', '/admin/order/', '_iframe', '102', 'layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('104', '报表', '0', null, null, null, '0', 'layui-icon layui-icon-table', '10', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('105', '充值报表', '1', 'admin:report:recharge', '/admin/report/recharge/', '_iframe', '104', 'layui-icon layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('106', '收益报表', '1', 'admin:report:income', '/admin/report/income/', '_iframe', '104', 'layui-icon ', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('109', '会话管理', '1', 'admin:session:main', '/admin/session/', '_iframe', '1', 'layui-icon ', '9', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('110', '踢下线', '2', 'admin:session:kickout', null, null, '109', 'layui-icon ', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('111', '冻结会话', '2', 'admin:session:freeze', null, null, '109', 'layui-icon ', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');
INSERT INTO `admin_power` VALUES ('112', '小说数据统计报表', '1', 'admin:report:book_statistics', '/admin/report/book_statistics', '_iframe', '104', 'layui-icon layui-icon ', '3', '2023-04-30 18:00:00', '2023-04-30 18:00:00', '1');

-- ----------------------------
-- Table structure for admin_role
-- ----------------------------
DROP TABLE IF EXISTS `admin_role`;
CREATE TABLE `admin_role` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `name` varchar(255) DEFAULT NULL COMMENT '角色名称',
  `code` varchar(255) DEFAULT NULL COMMENT '角色标识',
  `enable` int DEFAULT NULL COMMENT '是否启用',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  `details` varchar(255) DEFAULT NULL COMMENT '详情',
  `sort` int DEFAULT NULL COMMENT '排序',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of admin_role
-- ----------------------------
INSERT INTO `admin_role` VALUES ('1', '超级管理员', 'admin', '0', null, '管理员', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_role` VALUES ('2', '普通用户', 'common', '1', null, '只有查看，没有增删改权限', '2', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_role` VALUES ('3', '用户管理员', 'user', '1', null, '用户管理员', '3', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
-- ----------------------------
-- Table structure for admin_role_power
-- ----------------------------
DROP TABLE IF EXISTS `admin_role_power`;
CREATE TABLE `admin_role_power` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '标识',
  `power_id` int DEFAULT NULL COMMENT '用户编号',
  `role_id` int DEFAULT NULL COMMENT '角色编号',
  PRIMARY KEY (`id`),
  KEY `power_id` (`power_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `admin_role_power_ibfk_1` FOREIGN KEY (`power_id`) REFERENCES `admin_power` (`id`),
  CONSTRAINT `admin_role_power_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `admin_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of admin_role_power
-- ----------------------------
INSERT INTO `admin_role_power` VALUES ('12', '3', '2');
INSERT INTO `admin_role_power` VALUES ('13', '4', '2');
INSERT INTO `admin_role_power` VALUES ('14', '9', '2');
INSERT INTO `admin_role_power` VALUES ('15', '12', '2');
INSERT INTO `admin_role_power` VALUES ('16', '13', '2');
INSERT INTO `admin_role_power` VALUES ('18', '18', '2');
INSERT INTO `admin_role_power` VALUES ('19', '44', '2');
INSERT INTO `admin_role_power` VALUES ('20', '48', '2');
INSERT INTO `admin_role_power` VALUES ('29', '69', '3');
INSERT INTO `admin_role_power` VALUES ('30', '80', '3');
INSERT INTO `admin_role_power` VALUES ('34', '81', '3');
INSERT INTO `admin_role_power` VALUES ('35', '82', '3');
INSERT INTO `admin_role_power` VALUES ('36', '83', '3');
INSERT INTO `admin_role_power` VALUES ('37', '84', '3');
INSERT INTO `admin_role_power` VALUES ('38', '85', '3');
INSERT INTO `admin_role_power` VALUES ('39', '86', '3');
INSERT INTO `admin_role_power` VALUES ('40', '70', '3');
INSERT INTO `admin_role_power` VALUES ('41', '71', '3');
INSERT INTO `admin_role_power` VALUES ('42', '72', '3');
INSERT INTO `admin_role_power` VALUES ('43', '73', '3');
INSERT INTO `admin_role_power` VALUES ('44', '74', '3');
INSERT INTO `admin_role_power` VALUES ('45', '75', '3');
INSERT INTO `admin_role_power` VALUES ('46', '76', '3');
INSERT INTO `admin_role_power` VALUES ('47', '77', '3');
INSERT INTO `admin_role_power` VALUES ('48', '78', '3');
INSERT INTO `admin_role_power` VALUES ('49', '79', '3');

-- ----------------------------
-- Table structure for admin_user
-- ----------------------------
DROP TABLE IF EXISTS `admin_user`;
CREATE TABLE `admin_user` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(20) DEFAULT NULL COMMENT '用户名',
  `realname` varchar(20) DEFAULT NULL COMMENT '真实名字',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  `password_hash` varchar(128) DEFAULT NULL COMMENT '哈希密码',
  `enable` int DEFAULT NULL COMMENT '启用',
  `dept_id` int DEFAULT NULL COMMENT '部门id',
  `create_at` datetime DEFAULT NULL COMMENT '创建时间',
  `update_at` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of admin_user
-- ----------------------------
INSERT INTO `admin_user` VALUES ('1', 'admin', '超级管理', 'http://127.0.0.1:5000/_uploads/photos/1617291580000.jpg', '要是不能把握时机，就要终身蹭蹬，一事无成！', 'pbkdf2:sha256:260000$QNgunPIA175pHHsT$548ab24ab466bd68544380f08bd9be8000ff35afb07c0364ea4c50e8bce8aebd', '1', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_user` VALUES ('2', 'test', '测试', 'http://127.0.0.1:5000/_uploads/photos/1617291580000.jpg', '要是不能把握时机，就要终身蹭蹬，一事无成！', 'pbkdf2:sha256:150000$cRS8bYNh$adb57e64d929863cf159f924f74d0634f1fecc46dba749f1bfaca03da6d2e3ac', '1', '1', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_user` VALUES ('3', 'wind', '风', 'http://127.0.0.1:5000/_uploads/photos/1617291580000.jpg', '要是不能把握时机，就要终身蹭蹬，一事无成！', 'pbkdf2:sha256:150000$skME1obT$6a2c20cd29f89d7d2f21d9e373a7e3445f70ebce3ef1c3a555e42a7d17170b37', '1', '7', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
INSERT INTO `admin_user` VALUES ('5', 'user01', 'user01', '/static/admin/admin/images/avatar.jpg', null, 'pbkdf2:sha256:260000$4VQRwBmQPHsnKCr4$6a0f28e0a6145650ae2b64d0af7e06938a1fdeb1b588de6d0e65c55bb82b9c0f', '1', '4', '2023-04-30 18:00:00', '2023-04-30 18:00:00');
-- ----------------------------
-- Table structure for admin_user_role
-- ----------------------------
DROP TABLE IF EXISTS `admin_user_role`;
CREATE TABLE `admin_user_role` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '标识',
  `user_id` int DEFAULT NULL COMMENT '用户编号',
  `role_id` int DEFAULT NULL COMMENT '角色编号',
  PRIMARY KEY (`id`),
  KEY `role_id` (`role_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `admin_user_role_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `admin_role` (`id`),
  CONSTRAINT `admin_user_role_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `admin_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of admin_user_role
-- ----------------------------
INSERT INTO `admin_user_role` VALUES ('3', '1', '1');
INSERT INTO `admin_user_role` VALUES ('4', '2', '2');
INSERT INTO `admin_user_role` VALUES ('6', '5', '3');
INSERT INTO `admin_user_role` VALUES ('7', '5', '2');

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('a2796a5f85ea');

-- ----------------------------
-- Table structure for apscheduler_jobs
-- ----------------------------
DROP TABLE IF EXISTS `apscheduler_jobs`;
CREATE TABLE `apscheduler_jobs` (
  `id` varchar(191) NOT NULL,
  `next_run_time` double DEFAULT NULL,
  `job_state` blob NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_apscheduler_jobs_next_run_time` (`next_run_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of apscheduler_jobs
-- ----------------------------
