class UCLTablePartitioning:
    @staticmethod
    def get_range_partition_sql(table_name="analytics_uclstats"):
        sql_query = f"""
        ALTER TABLE {table_name}
        PARTITION BY RANGE (year) (
            PARTITION p_1993_1997 VALUES LESS THAN (1998),
            PARTITION p_1998_2002 VALUES LESS THAN (2003),
            PARTITION p_2003_2007 VALUES LESS THAN (2008),
            PARTITION p_2008_2012 VALUES LESS THAN (2013),
            PARTITION p_2013_2016 VALUES LESS THAN (2017),
            PARTITION p_2017_2020 VALUES LESS THAN (2021),
            PARTITION p_max VALUES LESS THAN MAXVALUE
        );
        """
        return sql_query.strip()