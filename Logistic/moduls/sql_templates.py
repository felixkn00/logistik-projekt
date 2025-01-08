class SQLTemplates:
    logger = {
        "database": {
            "add_database_error": "INSERT INTO"
        },
        "user": {
            "add_user_action": "INSERT INTO"
        }
    }

    user = {
        "get_permissions": "SELECT `can_create`, `can_read`, `can_update`, `can_delete`, `isSuperuser` FROM `user_account` WHERE `UserID` = %s",
        "set_permissions": """
            SELECT 
                `can_create`,
                `can_read`,
                `can_update`,
                `can_delete`,
                `isSuperuser`
            FROM 
                `user_account`
            WHERE 
                `UserID` = %s
        """,
        "update_permissions": "",
        "show_if_username_forgiven": "SELECT count(*) FROM `user_account` WHERE `Username` = %s",
        "get_users": "SELECT * FROM `user_account`",
        "add_user": "INSERT INTO `user_account` (`Username`,`Password`,`can_create`,`can_read`,`can_update`,`can_delete`) VALUES (%s, %s, %s, %s, %s, %s)",
        "remove_user": ""
    }

    deliveries = {
        "get_deliveries": "SELECT * FROM `deliveries`",
        "add_deliveries": "INSERT INTO `deliveries` (`DeliveryNumber`, `SupplierName`, `Information`, `Price`, "
                          "`DeliveryStatus`, `DeliveryDate`, `UserID`) VALUES (%s, %s, %s, %s, %s, %s, %s);",
        "update_deliveries": "UPDATE `deliveries` SET `DeliveryNumber`=%s, `SupplierName`=%s, `Information`=%s, "
                             "`Price`=%s, `DeliveryStatus`=%s, `DeliveryDate`=%s, `UserID`=%s WHERE `DeliveryID`=%s",
        "delete_deliveries_delete_foreign_key_elements": "DELETE FROM `delivery_details` WHERE `DeliveryID` = %s",
        "delete_deliveries": "DELETE FROM `deliveries` WHERE `DeliveryID` =%s",
        "details": {
            "get_delivery_details": "SELECT * FROM `delivery_details` WHERE `DeliveryID` =%s",
            "add_delivery_details": "INSERT INTO `delivery_details`(`DeliveryID`, `Article`, `Quantity`, "
                                    "`SinglePrice`, `GraduatedPrice`, `UserID`) VALUES (%s, %s, %s, %s, %s, %s);",
            "delete_delivery_details": "DELETE FROM `delivery_details` WHERE `DeliveryItemID` = %s",
            "update_delivery_details": "UPDATE `delivery_details` SET `Article`=%s, "
                                       "`Quantity`=%s, `SinglePrice`=%s, GraduatedPrice=%s, `UserID`=%s "
                                       "WHERE `DeliveryItemID`=%s"
        }

    }

    inventory = {
        "check_item_number": "SELECT count(`ItemID`) as count FROM `inventory` WHERE `ItemNumber` = %s",
        "select_item_by_ItemID": "SELECT * FROM `inventory` WHERE `ItemID` = %s",
        "get_inventory": "SELECT * FROM `inventory` WHERE `moved` IS NOT TRUE",
        "add_inventory": "INSERT INTO `inventory`( `ItemNumber`, `ItemName`, `Category`, `StockQuantity`, "
                         "`SinglePrice`, `GraduatedPrice`, `ExpiryDate`, `UserID`) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
        "update_inventory": "UPDATE `inventory` SET `ItemNumber`=%s, `ItemName`=%s, `StockQuantity`=%s, "
                            "`SinglePrice`=%s, `GraduatedPrice`=%s, `ExpiryDate`=%s, `UserID`=%s WHERE `ItemID`=%s",
        "delete_inventory": "DELETE FROM `inventory` WHERE `ItemID` = %s",
        "delete_inventory_foreign_key_elements": "DELETE FROM `scarce_commodity` WHERE `ItemID` = %s",
        "move_to_scarce_commodity_inventory": "UPDATE `inventory` SET `moved` = true WHERE `ItemID` = %s",
        "put_back_from_scare_commodity_inventory": "UPDATE `inventory` SET `moved` = false WHERE `ItemID` = %s"
    }

    scare_commodity_inventory = {
        "show_if_item_is_inside": "SELECT count(*) FROM `scarce_commodity` WHERE `ItemID` = %s",
        "get_inventory": """
                SELECT 
                    `inventory`.`ItemID`, 
                    `inventory`.`ItemNumber`, 
                    `inventory`.`ItemName`, 
                    `inventory`.`StockQuantity`,
                    `inventory`.`Category`, 
                    `inventory`.`SinglePrice`, 
                    `inventory`.`GraduatedPrice`, 
                    `inventory`.`ExpiryDate`, 
                    `inventory`.`UserID`, 
                    `scarce_commodity`.`StorageID`, 
                    `scarce_commodity`.`Donated`, 
                    `scarce_commodity`.`ThrownAway`, 
                    `scarce_commodity`.`Returned`, 
                    `scarce_commodity`.`Repaired`, 
                    `scarce_commodity`.`UserID`
                FROM 
                    `inventory`
                JOIN 
                    `scarce_commodity` ON `scarce_commodity`.`ItemID` = `inventory`.`ItemID`
                WHERE 
                    `inventory`.`moved` = true;
            """,
        "add_scare_commodity_inventory": "INSERT INTO `scarce_commodity`(`ItemID`, UserID) VALUES (%s, %s)",
        "update_scarce_commodity_inventory": """
            UPDATE 
                `inventory`
            JOIN 
                `scarce_commodity` ON `scarce_commodity`.`ItemID` = `inventory`.`ItemID`
            SET
                `inventory`.`ItemNumber` = %s,
                `inventory`.`ItemName` = %s,
                `inventory`.`Category` = %s,
                `inventory`.`StockQuantity` = %s,
                `inventory`.`SinglePrice` = %s,
                `inventory`.`GraduatedPrice` = %s,
                `inventory`.`ExpiryDate` = %s,
                `inventory`.`UserID` = %s,
                `scarce_commodity`.`Donated` = %s,
                `scarce_commodity`.`ThrownAway` = %s,
                `scarce_commodity`.`Returned` = %s,
                `scarce_commodity`.`Repaired` = %s,
                `scarce_commodity`.`UserID` = %s
            WHERE
                `inventory`.`ItemID` = %s AND `inventory`.`moved` = true;
        """,
        "delete_scarce_commodity": "DELETE FROM `scarce_commodity` WHERE `ItemID` = %s"

    }



