from datetime import datetime

def log(title: str, message: str, with_timestamp: bool = True, save_to_file: bool = True) -> None:
    """
    Logs for debugging

    Args:
        title (str): Log title
        message (str): Log description
        with_timestamp (bool, optional): With time mark or without. Defaults to True.
        save_to_file (bool, optional): Logs is saving to file (logs.txt). Defaults to True.
    """
    
    text = ""
    if with_timestamp:
        now = datetime.now()
        formatted = now.strftime("%d.%m.%Y %H:%M:%S.") + f"{now.microsecond:03d}"
        text = f"({formatted}) {title}: {message}"
    else:
        text = f"({title}: {message}"
    print(text)

    if save_to_file:
        with open("logs.txt", 'a') as file:
            file.write(f'{text}\n')