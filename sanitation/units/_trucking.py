#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Sanitation Explorer: Sustainable design of non-sewered sanitation technologies
Copyright (C) 2020, Sanitation Explorer Development Group

This module is developed by:
    Yalin Li <zoe.yalin.li@gmail.com>

This module is under the UIUC open-source license. Please refer to 
https://github.com/QSD-for-WaSH/sanitation/blob/master/LICENSE.txt
for license details.

Ref:
    [1] Trimmer et al., Navigating Multidimensional Social–Ecological System
        Trade-Offs across Sanitation Alternatives in an Urban Informal Settlement.
        Environ. Sci. Technol. 2020, 54 (19), 12641–12653.
        https://doi.org/10.1021/acs.est.0c03296.

'''

# %%

from warnings import warn
from .. import SanUnit, Transportation

__all__ = ('Trucking',)


class Trucking(SanUnit):
    '''For transportation of materials with considerations on material loss.'''
    
    def __init__(self, ID='', ins=None, outs=(),
                 load_type='mass', load=1., load_unit='m3',
                 distance=1., distance_unit='km',
                 interval=1., interval_unit='day',
                 fee=0.,
                 if_material_loss=True, loss_ratio=0.02):
        '''

        Parameters
        ----------
        load_type : [str]
            Either 'mass' or 'm3'.
        load : [float]
            Transportation load per trip.
        load_unit : [str]
            Unit of the load.
        distance : [float]
            Transportation distance per trip.
        distance_unit : [float]
            Unit of the distance.
        interval : [float]
            Time interval between trips.
        fee : [float]
            Transportation fee.
        if_material_loss : [bool]
            If material loss occurs during transportation.
        loss_ratio : [float] or [dict]
            Fractions of material losses due to transportation.

        '''
        SanUnit.__init__(self, ID, ins, outs)
        self.transportation = (
            Transportation(item='Trucking',
                           load_type=load_type, load=load, load_unit=load_unit,
                           distance=distance, distance_unit=distance_unit,
                           interval=interval, interval_unit=interval_unit,
                           fee=fee),
            )

        self.if_material_loss = if_material_loss
        self.loss_ratio = loss_ratio

    __doc__ += __init__.__doc__
    __init__.__doc__ = __doc__
    
    _N_ins = 1
    _N_outs = 2

    def _run(self):
        transported, loss = self.outs
        transported.copy_like(self.ins[0])
        loss.empty()
        if self.if_material_loss:
            if self._loss_ratio_type == 'float':
                loss.copy_like(transported)
                transported.mass *= 1 - self.loss_ratio
                loss.mass = self.ins[0].mass - transported.mass
            else:
                for cmp, ratio in self.loss_ratio.items():                        
                    transported.imass[cmp] *= 1 - ratio
                    loss.imass[cmp] = self.ins[0].imass[cmp] - transported.imass[cmp]

    def _design(self):
        pass

    def _cost(self):
        trucking = self.transportation[0]
        self._OPEX = trucking.cost/trucking.interval/24

            
    # @property
    # def capacity(self):
    #     '''[float] Capacity of the transportation vehicle, [m3].'''
    #     return self._capacity
    # @capacity.setter
    # def capacity(self, i):
    #     self._capacity = float(i)

    # @property
    # def distance(self):
    #     '''[float] Transportation distance, [km].'''
    #     return self._distance
    # @distance.setter
    # def distance(self, i):
    #     self._distance = float(i)

    # @property
    # def period(self):
    #     '''[float] Transportation time interval, [hr].'''
    #     return self._period
    # @period.setter
    # def period(self, i):
    #     self._period = float(i)

    # @property
    # def transport_cost(self):
    #     '''[float] Cost of transportation, [USD/km].'''
    #     return self._transport_cost
    # @transport_cost.setter
    # def transport_cost(self, i):
    #     self._transport_cost = float(i)
        
    # @property
    # def emptying_cost(self):
    #     '''[float] Cost of emptying the vehicle/container, [USD/emptying].'''
    #     return self._emptying_cost
    # @emptying_cost.setter
    # def emptying_cost(self, i):
    #     self._emptying_cost = float(i)

    # @property
    # def transport_impacts(self):
    #     '''[dict] Environmental impacts of transportation per km.'''
    #     return self._transport_impacts
    # @transport_impacts.setter
    # def transport_impacts(self, i):
    #     self._transport_impacts = i

    # @property
    # def emptying_impacts(self):
    #     '''[dict] Environmental impacts of emptying the vehicle/container each time.'''
    #     return self._emptying_impacts
    # @emptying_impacts.setter
    # def emptying_impacts(self, i):
    #     self._emptying_impacts = i
        
    @property
    def loss_ratio(self):
        '''
        [float] or [dict] Fractions of material losses due to transportation.
        If a single number is provided, then it is assumed that losses of
        all Components in the WasteStream are the same.
        
        Note
        ----
            Set state variable values (e.g., COD) will be retained if the loss
            ratio is a single number (treated like the loss stream is split
            from the original stream), but not when the ratio is a dict.

        '''
        return self._loss_ratio
    @loss_ratio.setter
    def loss_ratio(self, i):
        if not self.if_material_loss:
            msg = f'if_material_loss is False, the set value {i} is ignored.'
            warn(msg, source=self)
        try:
            self._loss_ratio = float(i)
            self._loss_ratio_type = 'float'
        except:
            if isinstance(i, dict):
                self._loss_ratio = i
                self._loss_ratio_type = 'dict'
            else:
                raise TypeError(f'Only float or dict allowed, not {type(i).__name__}.')












