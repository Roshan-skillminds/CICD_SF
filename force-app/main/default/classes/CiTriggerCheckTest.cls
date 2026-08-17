@IsTest(testFor='ApexClass:CiTriggerCheck')
private class CiTriggerCheckTest {
    @isTest
    static void testPing() {

        System.assertEquals('pong v10', CiTriggerCheck.ping());

    }
}
