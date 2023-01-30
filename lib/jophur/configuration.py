import board

class Configuration:
  def get():
    board_id = board.board_id

    if board_id == "adafruit_feather_rp2040":
      return Configuration(
        board_id = board_id,

        buttonA = board.D11,
        buttonB = board.D12,
        buttonC = board.D13,

        ledA = board.D24,
        ledB = board.D25,
        ledC = board.SCK,

        oledButtonA = board.D9,
        oledButtonB = board.D6,
        oledButtonC = board.D5,

        pedalAnalogIn = board.A0,

        rotaryButton = board.A1,
        rotaryEncoder1 = board.A2,
        rotaryEncoder2 = board.A3,
      )

    else:
      print("unknown", board_id)
      return Configuration(
        board_id = board_id,

        buttonA = board.D10,
        buttonB = board.D11,
        buttonC = board.D12,

        ledA = board.A5,
        ledB = board.D4,
        ledC = board.D13,

        oledButtonA = board.D9,
        oledButtonB = board.D6,
        oledButtonC = board.D5,

        pedalAnalogIn = board.A0,

        rotaryButton = board.A2,
        rotaryEncoder1 = board.A3,
        rotaryEncoder2 = board.A4,
      )

  def __init__(
      self,
      board_id=None,

      # button taps
      buttonA=None,
      buttonB=None,
      buttonC=None,

      # button LEDs
      ledA=None,
      ledB=None,
      ledC=None,

      # Expression pedal
      pedalAnalogIn=None,

      # OLED screen buttons
      oledButtonA=None,
      oledButtonB=None,
      oledButtonC=None,

      # Rotary Encoder
      rotaryButton=None,
      rotaryEncoder1=None,
      rotaryEncoder2=None,
  ):
    self.board_id = board_id
    self.buttonA = buttonA
    self.buttonB = buttonB
    self.buttonC = buttonC
    self.ledA = ledA
    self.ledB = ledB
    self.ledC = ledC
    self.pedalAnalogIn = pedalAnalogIn
    self.oledButtonA = oledButtonA
    self.oledButtonB = oledButtonB
    self.oledButtonC = oledButtonC
    self.rotaryButton = rotaryButton
    self.rotaryEncoder1 = rotaryEncoder1
    self.rotaryEncoder2 = rotaryEncoder2
