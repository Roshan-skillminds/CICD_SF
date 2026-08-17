@IsTest(testFor='ApexClass:CiTriggerCheck')
private class CiTriggerCheckTest {
    @isTest
    static void testPing() {

        System.assertEquals('pong v11', CiTriggerCheck.ping());

    }
}
