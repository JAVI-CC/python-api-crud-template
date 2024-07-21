from datetime import datetime

def date_format_client_to_server(date_format: str) -> datetime:
  return datetime.strptime(date_format, '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')


def date_format_server_to_client(date_format: str) -> datetime:
  return datetime.strptime(date_format, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y %H:%M:%S')