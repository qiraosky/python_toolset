/*
Navicat SQLite Data Transfer

Source Server         : DuplicateFileCleaner
Source Server Version : 30714
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 30714
File Encoding         : 65001

Date: 2017-06-02 18:14:37
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for tq_file
-- ----------------------------
DROP TABLE IF EXISTS "main"."tq_file";
CREATE TABLE "tq_file" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"name"  TEXT NOT NULL,
"md5code"  TEXT,
"suffix"  TEXT,
"create_time"  TEXT,
"update_time"  TEXT,
"oper_time"  TEXT,
"status"  TEXT,
"comment"  TEXT,
"desc"  TEXT
);

-- ----------------------------
-- Indexes structure for table tq_file
-- ----------------------------
CREATE UNIQUE INDEX "main"."md5code"
ON "tq_file" ("md5code" ASC);
