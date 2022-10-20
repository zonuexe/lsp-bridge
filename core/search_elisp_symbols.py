#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2022 Andy Stewart
# 
# Author:     Andy Stewart <lazycat.manatee@gmail.com>
# Maintainer: <lazycat.manatee@gmail.com> <lazycat.manatee@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import threading
import os
import traceback
import sexpdata

from core.utils import get_emacs_vars, message_emacs, eval_in_emacs, logger


class SearchElispSymbols:
    
    def __init__(self) -> None:
        self.search_ticker = 0
        self.search_thread_queue = []
        self.search_max_number = 100
        self.symbols = []
        
    def search(self, prefix: str, symbols):
        if len(symbols) > 0:
            self.symbols = symbols
        
        ticker = self.search_ticker + 1
        self.search_ticker = ticker
        
        search_thread = threading.Thread(target=lambda: self.search_symbols(prefix, ticker))
        search_thread.start()
        self.search_thread_queue.append(search_thread)
        
    def search_symbols(self, prefix: str, ticker: int):
        candidates = []
        for symbol in self.symbols:
            if symbol.startswith(prefix):
                candidates.append(symbol)
                    
                if len(candidates) > self.search_max_number:
                    break
                
        if ticker == self.search_ticker:
            eval_in_emacs("lsp-bridge-search-elisp-symbols--record-items", sorted(candidates, key=len))