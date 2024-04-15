import uasyncio as asyncio

TESTING = False

if TESTING:
    import tx_test
    asyncio.run(tx_test.main())
else:
    import gamepad_qt
    gamepad_qt.main()


