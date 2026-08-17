@IsTest(testFor='ApexClass:CiTriggerCheck')
private class CiTriggerCheckTest {
    @isTest
    static void testPing() {

        System.assertEquals('pong v9', CiTriggerCheck.ping());

    }
}
