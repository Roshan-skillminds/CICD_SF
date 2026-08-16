@IsTest
private class HelloWorldServiceTest {
    @IsTest
    static void greetsByName() {
        String result = HelloWorldService.greet('Roshan');
        System.assertEquals('Hello, Roshan!', result );
    }

    @IsTest
    static void greetsDefaultWhenBlank() {
        String result = HelloWorldService.greet(null);
        System.assertEquals('Hello, World!', result);
    }
}
