import board

class Configuration:
  board_id = None

  buttonA = None
  buttonB = None
  buttonC = None

  ledA = None
  ledB = None
  ledC = None

  oledButtonA = None
  oledButtonB = None
  oledButtonC = None

  rotaryButton = None
  rotaryEncoder1 = None
  rotaryEncoder2 = None
  
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

        rotaryButton = board.A1,
        rotaryEncoder1 = board.A2,
        rotaryEncoder2 = board.A3
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

        rotaryButton = board.A2,
        rotaryEncoder1 = board.A3,
        rotaryEncoder2 = board.A4,
      )

  def __init__(self, **kwargs):
    self.board_id = kwargs.get('board_id')

    # button taps
    self.buttonA = kwargs.get('buttonA')
    self.buttonB = kwargs.get('buttonB')
    self.buttonC = kwargs.get('buttonC')

    # button LEDs
    self.ledA = kwargs.get('ledA')
    self.ledB = kwargs.get('ledB')
    self.ledC = kwargs.get('ledC')

    # OLED screen buttons
    self.oledButtonA = kwargs.get('oledButtonA')
    self.oledButtonB = kwargs.get('oledButtonB')
    self.oledButtonC = kwargs.get('oledButtonC')

    # Rotary
    self.rotaryButton = kwargs.get('rotaryButton')
    self.rotaryEncoder1 = kwargs.get('rotaryEncoder1')
    self.rotaryEncoder2 = kwargs.get('rotaryEncoder2')
