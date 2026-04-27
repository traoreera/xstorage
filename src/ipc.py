

from xcore.sdk import action, AutoDispatchMixin, validate_payload
from .schemas import WRITEFILE, FILESMANIP, ZIPFILE, INSTALLMODULE
from .storage import StorageFile

class IPCCommands(StorageFile,AutoDispatchMixin):

    
    @action('xstorage.create')
    @validate_payload(WRITEFILE, type_response='model', unset=False)
    async def _create(self, payload):
        return await self.write(payload)
    
    @action('xstorage.read')
    @validate_payload(FILESMANIP, type_response='model', unset= False)
    async def _read(self, payload):
        return await self.read(payload)
    
    @action('xstorage.exist')
    @validate_payload(FILESMANIP, type_response='model',unset=False)
    async def _exist(self, payload):
        return await self.exists(payload)
    
    @action('xstorage.delete')
    @validate_payload(FILESMANIP,type_response='model', unset=False)
    async def _delete(self, payload):
        return await self.delete(payload)
    
    @action('xstorage.list.ext')
    @validate_payload(FILESMANIP, type_response='model', unset=False)
    async def _lists(self, payload):
        return await self.list(payload)
    

    @action('xstorage.original_name')
    @validate_payload(FILESMANIP, type_response='model', unset=False)
    async def _get_original_file_name(self, payload):
        return await self.original_name(payload)

    @action('xstorage.zip')
    @validate_payload(ZIPFILE, type_response='model', unset=False)
    async def _zip(self, payload):
        return await self.zip_files(payload)

    @action('xstorage.install_module')
    @validate_payload(INSTALLMODULE, type_response='model', unset=False)
    async def _install(self, payload):
        return await self.install_module(payload)