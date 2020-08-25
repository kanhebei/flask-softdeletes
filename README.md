# flask-softdeletes

## 介绍
flask-softdeletes
基于flask-sqlalchemy的软删除实现

## 使用简介

### 1.安装
<code>pip install flask-softdeletes</code>

### 2.导入 SoftDeletedMixin  

<code>from flask_softdeletes import SoftDeletedMixin</code>  

### 3.模型类继承 SoftDeletedMixin  

<code>class DemoModel(SoftDeletedMixin, db.Model):pass</code>

### 4.使用查询

[查询正常的数据,不包含已被软删除数据]   
<code> DemoModel.query</code>  

[只查询已经被软删除的数据]   
<code> DemoModel.query.only_trashed</code>  

[查询所有的数据, 包括已被软删除的和没有被软删除的数据]   
<code> DemoModel.query.with_trashed</code>  

[软删除数据]    

<code> demo = DemoModel.query.get(1)</code>  

<code> demo.delete() </code>

[恢复软删除的数据]   

<code> demo = DemoModel.query.with_trashed.get(1)</code>  

<code> demo.restore() </code>