# This file (templates.md) is for a sort of quick and easy copy and paste while I code to make things easier 

INFO LOGGING

            log_entry = create_log(
                level="INFO",
                message="NAME ran successfully",
                where="NAME",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write_to("C:/Users/Drags Jrs/Drags/Database/log/player_report_log.json", log_entry)



ERROR LOGGING

            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="NAME failed",
                where="NAME",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write_to("C:/Users/Drags Jrs/Drags/Database/log/player_report_log.json", log_entry)
            return log_entry