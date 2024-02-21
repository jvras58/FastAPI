from enum import Enum


class EnumOperationCode(Enum):
    # --------------------- Assignment ---------------------
    OP_1010001 = '1010001'   # Assignment - Create
    OP_1010002 = '1010002'   # Assignment - Update
    OP_1010003 = '1010003'   # Assignment - List
    OP_1010004 = '1010004'   # Assignment - Delete
    OP_1010005 = '1010005'   # Assignment - View
    # --------------------- Authorization ---------------------
    OP_1020001 = '1020001'   # Authorization - Create
    OP_1020002 = '1020002'   # Authorization - Update
    OP_1020003 = '1020003'   # Authorization - List
    OP_1020004 = '1020004'   # Authorization - Delete
    OP_1020005 = '1020005'   # Authorization - View
    # --------------------- Transaction ---------------------
    OP_1030001 = '1030001'   # Transaction - Create
    OP_1030002 = '1030002'   # Transaction - Update
    OP_1030003 = '1030003'   # Transaction - List
    OP_1030004 = '1030004'   # Transaction - Delete
    OP_1030005 = '1030005'   # Transaction - View
    # --------------------- User ---------------------
    OP_1040001 = '1040001'   # User - Create
    OP_1040002 = '1040002'   # User - Update
    OP_1040003 = '1040003'   # User - List
    OP_1040004 = '1040004'   # User - Delete
    OP_1040005 = '1040005'   # User - View
    OP_1040006 = '1040006'   # User - Transactions granted
    # --------------------- Role ---------------------
    OP_1050001 = '1050001'   # Role - Create
    OP_1050002 = '1050002'   # Role - Update
    OP_1050003 = '1050003'   # Role - List
    OP_1050004 = '1050004'   # Role - Delete
    OP_1050005 = '1050005'   # Role - View
