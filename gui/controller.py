from view import View
import os, re
import copy
# Regular expression to check for legal message formatting
LEGAL_MSG = re.compile("^([0-9]+,[0-9]+,)([a-z]+=[a-z]+,?){0,}")

class Controller():
  def __init__(self, rows, cols):
    self.rows, self.cols = rows, cols
    self._model = []
    for x in range(0,rows):
      self._model.append([None] * cols)
    self.blank = {'iamhere':False, 'west':False, 'north':False, 'east':False, 'south':False, 'tshape':'none', 'tcolor':'none', 'robot':False, 'explored':False}
    for r in range(0,rows):
      for c in  range(0, cols):
        self._model[r][c] = copy.deepcopy(self.blank)
    self._view = View(rows, cols, open_browser=True)

  def _update_model(self, row, col, attrs):
    for r in range(0,self.rows):
      for c in range(0,self.cols):
        self._model[r][c]['iamhere'] = False
    for k,v in attrs.items():
      self._model[row][col][k] = v
    self._model[row][col]['explored'] = True

  def _update_view(self, row, col, cell_state):
    self._view.update_cell(row, col, cell_state)

  def handle_msg(self, msg):
    # For simplicity, all messages are handled in lower-case
    msg = msg.lower()
    # reset is a special message that sets the GUI back to its intial state
    if 'reset' in msg:
      self.reset()
    elif LEGAL_MSG.match(msg):
      tokens = msg.split(',')
      # Drop empty tokens resulting from extra commas
      tokens = filter(lambda t: t, tokens)
      # Structure the tokens to be passed to the model
      row, col = int(tokens[0]), int(tokens[1])
      attrs = {'iamhere' : True}
      # iamhere=true is automatically added to the message to save you from 
      # sending this with your messages; if you are sending information about
      # some cell other than where you are located currently, you MUST send 
      # iamhere=false
      for t in tokens[2:]:
        attr, val = t.split('=')
        # Convert to a boolean if that's the intention indicated by val
        val = True if 'true' in val else False if 'false' in val else val
        attrs[attr] = val
      print attrs
      # Ensure legal coordinates
      if row < self.rows and col < self.cols and row >= 0 and col >= 0:
        # Update the model and get the new state of the cell
        self._update_model(row, col, attrs)
        # Update the view with the full maze state; this is necessary now that 
        # we are tracking dynamic state (robot position)
        self._view.render(self._model)
      else:
        print 'Message ignored: Illegal maze coordinates: (%d, %d).' % (row, col)
    else:
      print 'Message ignored: Does not match the API requirements.'

  def reset(self):
    self._model = []
    for x in range(0,self.rows):
      self._model.append([None] * self.cols)
    for r in range(0,self.rows):
      for c in  range(0, self.cols):
        self._model[r][c] = copy.deepcopy(self.blank)
    self._view = View(self.rows, self.cols)
