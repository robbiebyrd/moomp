# from models.portal import PortalCreateDTO, PortalUpdateDTO
# from services.portal import PortalService
# from utils.db import connect_db
#
# connect_db()
#
#
# def create_test_portal(portal_name: str, from_id: str | None = None):
#     portal = PortalCreateDTO(
#         name=portal_name,
#         from_id=from_id,
#         visible=True
#     )
#     PortalService.register(portal)
#     return
#
#
# def cleanup_test_portal(username: str):
#     PortalService.remove(username)
#     return
#
#
# def test_create_portal():
#     create_test_portal('Test')
#     cs = PortalService.get_by_username('Test')
#     assert cs.name == 'Test'
#     assert cs.email == 'Test@Test.com'
#     cleanup_test_portal('Test')
#
#
# def test_update_portal():
#     create_test_portal('Test')
#     csu = PortalService.new('Test')
#     csu.update(
#         user=PortalUpdateDTO(
#             name="Test2",
#             display="Test User Test2",
#         )
#     )
#     cs = PortalService.get_by_username('Test2')
#
#     assert cs.name == 'Test2'
#     assert cs.display == 'Test User Test2'
#
#     cleanup_test_portal('Test2')
#
#
# def test_remove_portal():
#     create_test_portal('deleteme')
#     PortalService.remove('deleteme')
#
#     assert PortalService.get_by_username(
#         username='Test') is None
#     cleanup_test_portal('deleteme')
#
#
# def test_rename_portal():
#     create_test_portal('RenameMe')
#     cs = PortalService.new('RenameMe')
#     cs.rename('YouRenamedMe')
#
#     assert PortalService.get_by_username(
#         username='YouRenamedMe') is not None
#     assert PortalService.get_by_username(
#         username='RenameMe') is None
#     cleanup_test_portal('YouRenamedMe')
#
#
# def test_update_portal_properties():
#     create_test_portal('PropertyUser')
#     cs = PortalService(PortalService.get_by_username('PropertyUser'))
#     cs.update_property({"test": "test"})
#
#     assert PortalService.get_by_username(
#         username='PropertyUser').properties == {"test": "test"}
#
#     cleanup_test_portal('PropertyUser')
