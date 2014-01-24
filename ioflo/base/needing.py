"""needing.py need action module

"""
#print "module %s" % __name__

import time
import struct
from collections import deque
import inspect



from .globaling import *
from .odicting import odict
from . import aiding
from . import excepting
from . import registering
from . import storing 
from . import acting
from . import tasking
from . import framing

from .consoling import getConsole
console = getConsole()


#Class definitions should be singletons or borgs
#instance should be only one should use singleton or borg

def CreateInstances(store):
    """Create action gloal lists and instances
       must be function so can recreate after clear registry
       globals good for module self tests
    """
    #special needs
    needDone = DoneNeed(name = 'needDone', store = store)
    needAlways = AlwaysNeed(name = 'needAlways', store = store)
    needStatus = StatusNeed(name = 'needStatus', store = store)
    needUpdate = UpdateNeed(name = 'needUpdate', store = store)
    needChange = ChangeNeed(name = 'needChange', store = store)

    #dynamic need types
    needBoolean = BooleanNeed(name = 'needBoolean', store = store)
    needDirect = DirectNeed(name = 'needDirect', store = store)
    needIndirect = IndirectNeed(name = 'needIndirect', store = store)


class Need(acting.Actor):
    """Need Class for conditions  such as entry or trans

    """
    Registry = odict()

    def expose(self):
        """

        """
        print "Need %s " % (self.name)

    @staticmethod
    def Check(state, comparison, goal, tolerance):
        """Check state compared to goal with tolerance
           tolerance ignored unless comparison == or !=

        """
        if comparison == '==':
            try: #in case goal is string
                result = ( (goal - abs(tolerance)) <= state <= (goal + abs(tolerance)))
            except TypeError:
                result = (goal == state)
        elif comparison == '<':
            result = ( state < goal)
        elif comparison == '<=':
            result = ( state <= goal)
        elif comparison == '>=':
            result = ( state >= goal)
        elif comparison == '>':
            result = ( state > goal)
        elif comparison == '!=':
            try: #in case goal is string
                result = ( state <= (goal - abs(tolerance)) or state >= (goal + abs(tolerance)) )
            except TypeError:
                result = (goal != state)
        else:
            result = False

        return result

#special needs
class AlwaysNeed(Need):
    """AlwaysNeed Need

       inherited attributes:

             .name = unique name for action instance
             .store = shared data store

       parameters:

    """
    def action(self, **kw):
        """Always return true"""

        result = True
        console.profuse("Need Always = {0}\n".format(result)) 

        return result


class DoneNeed(Need):
    """DoneNeed Need

       inherited attributes:

             .name = unique name for action instance
             .store = shared data store

       parameters:
          tasker
    """
    def action(self, tasker, **kw):
        """Check if  tasker done 

        """
        result = tasker.done
        console.profuse("Need Framer {0} done = {1}\n".format(tasker.name, result)) 

        return result
    
    def resolve(self, tasker, **kw):
        """Resolves value (tasker) link that is passed in as tasker parm
           resolved link is passed back to container act to update in act's parms
        """
        parms = super(DoneNeed, self).resolve( **kw) 

        if not isinstance(tasker, tasking.Tasker): # name of tasker so resolve
            if tasker not in tasking.Tasker.Names: 
                raise excepting.ResolveError("ResolveError: Bad need done aux link", tasker, self.name)
            tasker = tasking.Tasker.Names[tasker] #replace tasker name with tasker

        #if not tasker.schedule in [AUX, SLAVE]: 
            #raise excepting.ResolveError("ResolveError: Bad need done tasker not auxiliary or slave", tasker, self.name)

        parms['tasker'] = tasker #replace name with valid link

        return parms #return items are updated in original act parms
    
    
    def cloneParms(self, parms, clones, **kw):
        """ Returns parms fixed up for framing cloning. This includes:
            Reverting any Frame links to name strings,
            Reverting non cloned Framer links into name strings
            Replacing any cloned framer links with the cloned name strings from clones
            Replacing any parms that are acts with clones.
            
            clones is dict whose items keys are original framer names
            and values are duples of (original,clone) framer references
        """
        parms = super(StatusNeed,self).cloneParms(parms, clones, **kw)
        
        tasker = parms.get('tasker')
        
        if isinstance(tasker, tasking.Tasker):
            if tasker.name in clones:
                parms['tasker'] = clones[tasker.name][1].name
            else:
                parms['tasker'] = tasker.name # revert to name
        elif tasker: # assume namestring
            if tasker in clones:
                parms['tasker'] = clones[tasker][1].name
        
        return parms        

class StatusNeed(Need):
    """StatusNeed Need

       inherited attributes:

             .name = unique name for action instance
             .store = shared data store

       parameters:
          tasker
          status
    """
    def action(self, tasker, status, **kw):
        """Check if  tasker done """

        result = (tasker.status == status)
        console.profuse("Need Tasker {0} status is {1} = {2}\n".format(
            tasker.name, StatusNames[status], result)) 

        return result
    
    def resolve(self, tasker, **kw):
        """Resolves value (tasker) link that is passed in as parm
           resolved link is passed back to container act to update in act's parms
        """
        parms = super(StatusNeed, self).resolve( **kw) 

        if not isinstance(tasker, tasking.Tasker): #so name of tasker
            if tasker not in tasking.Tasker.Names: 
                raise excepting.ResolveError("ResolveError: Bad need done tasker link", tasker, self.name)
            tasker = tasking.Tasker.Names[tasker] #replace tasker name with tasker

        parms['tasker'] = tasker #replace name with valid link

        return parms #return items are updated in original act parms
    
    
    def cloneParms(self, parms, clones, **kw):
        """ Returns parms fixed up for framing cloning. This includes:
            Reverting any Frame links to name strings,
            Reverting non cloned Framer links into name strings
            Replacing any cloned framer links with the cloned name strings from clones
            Replacing any parms that are acts with clones.
            
            clones is dict whose items keys are original framer names
            and values are duples of (original,clone) framer references
        """
        parms = super(StatusNeed,self).cloneParms(parms, clones, **kw)
        
        tasker = parms.get('tasker')
        
        if isinstance(tasker, tasking.Tasker):
            if tasker.name in clones:
                parms['tasker'] = clones[tasker.name][1].name
            else:
                parms['tasker'] = tasker.name # revert to name
        elif tasker: # assume namestring
            if tasker in clones:
                parms['tasker'] = clones[tasker][1].name
        
        return parms    

class BooleanNeed(Need):
    """BooleanNeed Need

       if state
    """
    def action(self, state, stateField, **kw):
        """ Check if state[stateField] evaluates to True
            parameters:
              state = share of state
              stateField = field key

        """

        if state[stateField]:
            result = True
        else:
            result = False
        console.profuse("Need Boolean, if {0}[{1}]: = {2}\n".format(
            state.name, stateField, result)) 


        return result

class DirectNeed(Need):
    """DirectNeed Need

       if state comparison goal [+- tolerance]
    """

    def action(self, state, stateField, comparison, goal, tolerance, **kw):
        """ Check if state[field] comparison to goal +- tolerance is True
            parameters:
                state = share of state
                stateField = field key
                comparison
                goal
                tolerance

        """

        result = self.Check(state[stateField], comparison, goal, tolerance)
        console.profuse("Need Direct, if {0}[{1}] {2} {3} +- {4}: = {5}\n".format(
            state.name, stateField, comparison, goal, tolerance, result))     

        return result

class IndirectNeed(Need):
    """IndirectNeed Need

       if state comparison goal [+- tolerance]
    """
    def action(self, state, stateField, comparison, goal, goalField, tolerance, **kw):
        """ Check if state[field] comparison to goal[goalField] +- tolerance is True
                       parameters:
              state = share of state
              stateField = field key
              comparison
              goal
              goalField
              tolerance
        
        """

        result = self.Check(state[stateField], comparison, goal[goalField], tolerance)
        console.profuse("Need Indirect, if {0}[{1}] {2} {3}[{4}] +- %s: = {5}\n".format(
            state.name, stateField, comparison, goal, goalField, tolerance, result))     

        return result
    
class MarkerNeed(Need):
    """ MarkerNeed is base class for needs that insert markers on resolvelinks
        inherited attributes:
            .name = unique name for action instance
            .store = shared data store
        parms:
            share
            name
            frame       only used in resolvelinks
            marker      only used in resolvelinks
    
    """
    def resolve(self, share, name, frame, marker, **kw):
        """Resolves frame framename link and then
           inserts marker as first enact in the resolved frame
           
           If appropriate resolved link(s) are passed back to container act to
           update the act's parms
        """
        parms = super(MarkerNeed, self).resolve( **kw) 
        
        if not share.marks.get(name):
            share.marks[name] = storing.Mark()        
    
        if not isinstance(frame, framing.Frame): # must be pathname
            if frame not in framing.Frame.Names: 
                raise excepting.ResolveError("ResolveError: Bad need update frame link", frame, self.name)
            parms['frame'] = frame = framing.Frame.Names[frame] #replace frame name with frame
        
        if not isinstance(marker, acting.Marker): #marker is name of actor
            if marker not in acting.Actor.Names:
                raise excepting.ResolveError("ResolveError: Bad need marker link", marker, self.name)
            parms['marker'] = marker = acting.Actor.Names[marker]
        
        found = False
        for enact in frame.enacts:
            if (enact.actor is marker and
                    enact.parms['share'] is share and
                    enact.parms['name'] == name):
                found = True
                break
            
        if not found:
            markerParms = dict(share=share, name=name)
            markerAct = acting.Act(marker, parms=markerParms)
            
            frame.insertEnact(markerAct)
            console.profuse("     Added {0} {1} with {2} in {3}\n".format(
                'enact',
                markerAct.actor.name,
                markerAct.parms['share'].name,
                markerAct.parms['name']))   
                
        return parms #return items are updated in original act parms    
    
    def cloneParms(self, parms, clones, **kw):
        """ Returns parms fixed up for framing cloning. This includes:
            Reverting any Frame links to name strings,
            Reverting non cloned Framer links into name strings
            Replacing any cloned framer links with the cloned name strings from clones
            Replacing any parms that are acts with clones.
            
            clones is dict whose items keys are original framer names
            and values are duples of (original,clone) framer references
        """
        parms = super(MarkerNeed,self).cloneParms(parms, clones, **kw)
        
        share = parms.get('share')
        name = parms.get('name')
        frame = parms.get('frame')
        marker = parms.get('marker')
            
        if isinstance(frame, framing.Frame):
            parms['frame'] = frame.name # revert to name 

        return parms    
    
class UpdateNeed(MarkerNeed):
    """ UpdateNeed Need

        inherited attributes:
            .name = unique name for action instance
            .store = shared data store

        parameters:
            share
            name
            frame       only used in resolvelinks
            marker      only used in resolvelinks
    """
    def action(self, share, name, **kw):
        """ Check if share updated while in frame/mark denoted by name key if any
            Default is False
        """
        result = False
        mark = share.marks.get(name) #get mark from mark frame name key
        if mark and mark.stamp != None:
            result = share.stamp >= mark.stamp #equals so catch updates on enter
        
        console.profuse("Need Share {0} update in Frame {1} = {2}\n".format(
            share.name, name, result)) 

        return result

class ChangeNeed(MarkerNeed):
    """ChangeNeed Need
       inherited attributes:
            .name = unique name for action instance
            .store = shared data store

       parameters:
            share
            name
            frame       only used in resolvelinks
            marker      only used in resolvelinks
    """
    def action(self, share, name, **kw):
        """ Check if share data changed while in frame/mark denoted by name key if any
            Default is False
        """
        result = False
        mark = share.marks.get(name) #get mark from mark frame name key
        if mark and mark.data != None:
            for field, value in share.items():
                try:
                    if getattr(mark.data, field) != value:
                        result = True
                        
                except AttributeError as ex: # new attribute so changed
                    result = True
                
                if result: #stop checking on first change
                    break
                         
        
        console.profuse("Need Share {0} change in Frame {1} = {2}\n".format(
            share.name, name, result)) 

        return result

def Test():
    """Module Common self test

    """
    pass


if __name__ == "__main__":
    test()
