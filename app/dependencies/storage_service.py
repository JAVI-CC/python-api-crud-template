import aiofiles
import aiofiles.os
from fastapi import UploadFile


async def save_upload_file(file: UploadFile, path: str) -> bool:
    async with aiofiles.open(path, "wb") as out_file:
        await out_file.write(file.file.read())  # async write
        return True

async def delete_file(path: str) -> bool:
  is_exists_file = await aiofiles.os.path.isfile(path)

  if is_exists_file:
    await aiofiles.os.remove(path)
  
  return True