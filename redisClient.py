#Importações
import sys
import asyncio


# %%
# import urllib library


# %%

class RedisClient:
    async def connect(self, host, port):
        self.r, self.w = await asyncio.open_connection(host, port)
        
    async def set(self, key, value):
        self.w.write(f"SET {key} \"{value}\"\r\n".encode())
        await self.w.drain()

        return await self._read_reply()
    
    async def _read_reply(self):
        tag = await self.r.read(1)

        if tag == b'$':
            length = b''
            ch = b''

            while ch != b'\n':
                ch = await self.r.read(1)
                length += ch

            totalLength = int(length[:-1]) + 2

            result = b''
            while len(result) < totalLength:
                result += await self.r.read(totalLength - len(result ))
            return result[:-2].decode()
        
        if tag == b':':
            result = b''
            ch = b''

            while ch != b'\n':
                ch = await self.r.read(1) 
                result += ch
            return int(result[:-1].decode())
        
        if tag == b'-':
            result = b''
            ch = b''

            while ch != b'\n':
                ch = await self.r.read(1) 
                result += ch
            raise Exception(result[:-1].decode())
        
        if tag == b'+':
            result = b''
            ch = b''

            while ch != b'\n':
                ch = await self.r.read(1)
                result += ch
            return result[:-1].decode()
        else:
            msg = await self.r.read(100)
            raise Exception(f"Unknown tag: {tag}, msg: {msg}")
    
    async def get(self, key):
        self.w.write(f"GET {key}\r\n".encode())
        await self.w.drain()
        return await self._read_reply()

    async def incr(self, key):
        self.w.write(f"INCR {key}\r\n".encode())
        await self.w.drain()
        return await self._read_reply()

    async def send(self, *args):
        resp_args = "".join([f"${len(x)}\r\n{x}\r\n" for x in args])

        self.w.write(f"*{len(args)}\r\n{resp_args}".encode())
        await self.w.drain()
        return await self._read_reply()