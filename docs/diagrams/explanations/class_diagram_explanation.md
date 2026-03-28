## Class Diagram Explanation

The Class Diagram of the **Keymorpher AI System** represents the static structure of the system and shows the classes, their attributes, methods, and relationships. The design follows Object-Oriented principles and is derived from the OOSE analysis model.

### Entity Classes
- **User**
  - Attribute: `userId`
  - Represents the user interacting with the gesture-based virtual keyboard system.

- **VirtualKey**
  - Attributes: `keyLabel`, `position`
  - Represents an individual key of the virtual keyboard along with its on-screen position.

- **TypedText**
  - Attribute: `content`
  - Methods: `appendText()`, `deleteText()`
  - Stores and manages the text entered by the user through gesture-based key selection.

### Interface Classes
- **CameraInterface**
  - Attributes: `cameraId`
  - Methods: `startCamera()`, `captureFrame()`
  - Acts as an interface between the system and the physical camera to capture video frames.

- **KeyboardDisplay**
  - Attribute: `layoutType`
  - Methods: `renderKeyboard()`, `highlightKey()`
  - Responsible for rendering the virtual keyboard on the screen and highlighting selected keys.

- **TextDisplay**
  - Attribute: `fontSize`
  - Methods: `displayText()`, `clearText()`
  - Displays the typed text and provides options to clear or update the text on the screen.

### Control Classes
- **HandDetectionController**
  - Attribute: `handLandmarks`
  - Method: `detectHand()`
  - Detects the user’s hand and extracts landmark information using computer vision techniques.

- **GestureController**
  - Attribute: `gestureType`
  - Method: `analyzeGesture()`
  - Analyzes hand landmarks to interpret user gestures for key selection.

- **KeyPressController**
  - Attribute: `pressedKey`
  - Method: `registerKeyPress()`
  - Registers the selected virtual key based on detected gestures and updates the typed text.

- **SystemController**
  - Attribute: `systemState`
  - Methods: `startSystem()`, `stopSystem()`
  - Acts as the central controller responsible for managing system flow and coordination between different controllers.

### Relationships
The User interacts with the system through the **SystemController**. Interface classes communicate with control classes to handle input, processing, and output. Control classes coordinate among themselves and interact with entity classes to maintain system data and state.

This class diagram ensures modularity, clear separation of responsibilities, and ease of maintenance, making the system scalable and suitable for cross-platform implementation.
