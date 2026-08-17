@IsTest(testFor='ApexClass:MathUtils')
private class MathUtilsTest {
    @isTest
    static void testAddNumbers() {

        System.assertEquals(5, MathUtils.addNumbers(2, 3));

    }
}
