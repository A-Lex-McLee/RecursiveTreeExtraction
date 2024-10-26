#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 15:31:57 2024

@author: alexanderpfaff
"""

from dataclasses import dataclass


class Bracketing:
    def __init__(self, text: str) -> None:
        
        txt_raw = open(text, "r")
        psdText: str = txt_raw.read()
        txt: list[str] = psdText.split()
        tmpText: str = " ".join(txt)
        tmpText = tmpText.replace('(', ' ( ')
        tmpText = tmpText.replace(')', ' ) ')
        lastDot: int = text.rfind('.')
        self._fileID: str = text[:lastDot]
        self.__initializeS: bool = True
        self._sentences: list[str] = self._separateSentences(tmpText)
        self.__initializeS = False
        
    @property 
    def fileID(self):
        return self._fileID
        
    @property
    def sentences(self) -> list[str]:
        return self._sentences
    
    @sentences.setter 
    def sentences(self, sentences: list[str]) -> None:
        if self.__initializeS:
            self._sentences = sentences
        else:
            raise Exception("Illegal attempt to overwrite sentences!!!")
    @property 
    def size(self):
        return len(self._sentences)
        

    def getSentence(self, idx: int):
        return self.sentences[idx]
        
        
    def getTree(self, idx: int):
        sentence: str = self.getSentence(idx)
        return Tree(sentence)
        
        
    
    def _separateSentences(self, text: str) -> list[str]:

        assert text.count('(') == text.count(')')

        out: list[str] = []
        bracketPair: int = 0
        currentStart: int = text.find('(')
        charIdx: int = 0        
        while currentStart >= 0:
            if text[charIdx] == '(':
                bracketPair += 1
            if text[charIdx] == ')':
                bracketPair -= 1
            if bracketPair == 0:
                sequence: str = text[currentStart:charIdx+1]
                if sequence != "":
                    out.append(text[currentStart:charIdx+1])
                currentStart = text.find('(', charIdx) 
            charIdx += 1
        return tuple(out) 
    
    


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 


class TreeNode: 
    def __init__(self):
        self._category: str 
        self._item: str 
        self._level: int
        self._children: list[TreeNode] 
        # self._leftIdx
        self._restText: str # = clauseTxt
        self._bracketPairs: dict[int, int]

    def __str__(self) -> str:
        dist: str = self._level * " . ."
        outStr: str = f"{self._level:2d} {dist} {self._category}  {self._item} \n "
        return outStr
        

    @property 
    def category(self):
        return self._category

    @property 
    def item(self):
        return self._item

    @property 
    def level(self):
        return self._level

    @property 
    def children(self):
        return self._children

    @property 
    def bracketPairs(self):
        return self._bracketPairs


    def addChild(self, node) -> None:
        self._children.append(node)


    # TODO 
    def _grow(self, butcherText: str):
        childNodes: list[str] = self._checkChildren(butcherText)
        
        self.theKids: list[str] = childNodes[:]  #######

        for nodeStr in childNodes:
            if self._isTerminal(nodeStr):
                node: Node = self._makeTerminal(nodeStr)
                self.addChild(node)
            if self._isCatNode(nodeStr):
                node: catNode = self._makeCatNode(nodeStr)
                self.addChild(node)
            

            
            
            
        
    def _checkChildren(self, txtToParse: str):
        """
        @AUX-method

        Parameters
        ----------
        txtToParse : 
            D-type:     str
            U-type: 
            DESCRIPTION.

        Returns
        -------
        out : TYPE
            DESCRIPTION.

        """
        assert txtToParse.count('(') == txtToParse.count(')')
        bracketPairs = self._bracketIdxPairs(txtToParse)
        countIdx: int = 0
        auxCountIdx: int = countIdx
        out: list[str] = []
        while txtToParse.count('(') > 0 and countIdx < len(txtToParse):
            countIdx = txtToParse.find('(', auxCountIdx)
            if countIdx == -1:
                break
            endBracket: int = bracketPairs[countIdx]
            assert txtToParse[endBracket] == ')'
            out.append(txtToParse[countIdx+1:endBracket])
            auxCountIdx = endBracket + 1
        return out






    
    def _isTerminal(self, nodeStr: str) -> bool: 
        if nodeStr.count('(') != 0 or nodeStr.count(')') != 0:
            return False
        if nodeStr.isspace():
            return False
        return True

    def _makeTerminal(self, nodeStr: str):
        contentLst: list[str] = nodeStr.split()
        assert len(contentLst) == 2
        if not contentLst[0].isupper():
            cat: str = "<char>"
        else:
            cat: str = contentLst[0]
        return Node(self._level+1, cat, contentLst[1])


    def _isCatNode(self, nodeStr: str) -> bool:
        if nodeStr.count('(') == 0 and nodeStr.count(')') == 0:
            return False
        firstBracket: int = nodeStr.find('(')
        if nodeStr[:firstBracket].isspace():
            return False
        return True
        
    def _makeCatNode(self, nodeStr: str):
        assert nodeStr.count('(') == nodeStr.count(')')
        # bracketPairs: dict[int, int] = self._bracketIdxPairs(nodeStr)
        firstBracket: int = nodeStr.find('(')
        cat: str = nodeStr[:firstBracket].strip()
        return catNode(self.level+1, nodeStr[firstBracket:], cat)




    def _isDoubleOpen(self, text: str) -> bool:
        bracketIdx: int 
        nextBracket: str
        nextBracketIdx: int 
        nextNextBracket: str
        nextBracket, bracketIdx  = self._countIdx_to_nextBracket(text)      
        nextNextBracket, nextBracketIdx  = self._countIdx_to_nextBracket(text[bracketIdx+1])  
        if 0 <= bracketIdx < nextBracketIdx:
            if nextBracket == 'OPEN' and nextNextBracket == 'OPEN':
                interString: str = text[bracketIdx+1:nextBracketIdx]
                if interString.isspace():
                    return True
        return False

    def _countIdx_to_nextBracket(self, restString: str) -> tuple[str, int]:
        countIdx: int = 0        
        while countIdx < len(restString):
            if restString[countIdx] == '(':
                return 'OPEN', countIdx
            if restString[countIdx] == ')':
                return 'CLOSE', countIdx
            countIdx += 1
        return "", -1

    def _bracketIdxPairs(self, text : str) -> tuple:
        idx = text.find('(')
        left = [idx]
        idx += 1 
        out = dict()
        while left or idx < len(text)-1:
            if text[idx] == '(':
                left.append(idx)
            if text[idx] == ')':
                l = left.pop()
                out[l] = idx
            idx += 1
        return out
    



        



@dataclass
class catNode(TreeNode):
    def __init__(self, level: int, restString: str = '--', cat: str = '--'):
        super()
        self._category: str = cat
        self._item: str = '<< catP >>'
        self._level: int = level
        self._children: list[TreeNode] = []
        self._restText = restString
        self._bracketPairs: dict[int, int] = self._bracketIdxPairs(self._restText)
        self._grow(self._restText)
        


@dataclass
class Node(TreeNode):
    def __init__(self, level: int, cat: str = '--', item: str = '--'):
        super()
        self._category: str = cat
        self._item: str = item
        self._level: int = level
        self._children: list[TreeNode] = []
        self._restText = ""
        

@dataclass
class RootNode(TreeNode):    
    def __init__(self, clause: str):
        super()
        self._category: str
        self._item: str = '<< ROOT >>'
        self._level: int = 0
        self._children: list[TreeNode] = []
        self._restText: str = clause
        self._opendIdx: int 
        self.ID: str
        self._bracketPairs: dict[str, str] 

        self._activateA()
        self._activateB()
        self._activateC()

        self._bracketPairs: dict[str, str] = self._bracketIdxPairs(self._restText)
        
        _opendIdx, _closeIdx = self._getStartIdx()
        
        
        self._grow(_opendIdx, _closeIdx-1)




    def _grow(self, startIdx: int, endIdx: int):        
        
        childNodes: list[str] = self._checkChildren(self._restText, startIdx, endIdx)
        
        self.theKids: list[str] = childNodes[:]

        for nodeStr in childNodes:
            if self._isTerminal(nodeStr):
                node: Node = self._makeTerminal(nodeStr)
                self.addChild(node)
            if self._isCatNode(nodeStr):
                node: catNode = self._makeCatNode(nodeStr)
                self.addChild(node)
            
            
        
    def _checkChildren(self, txtToParse: str, startIdx: int, endIdx: int):
        countIdx: int = startIdx
        auxCountIdx: int = countIdx
        out: list[str] = []
        while txtToParse[countIdx:endIdx].count('(') > 0 and countIdx < endIdx:
            if txtToParse[countIdx] == '(':
                endBracket: int = self._bracketPairs[countIdx]
                assert txtToParse[endBracket] == ')'
                if txtToParse[auxCountIdx:countIdx].isspace():
                    out.append(txtToParse[countIdx+1:endBracket])
                else:
                    out.append(txtToParse[auxCountIdx:endBracket])
                countIdx =  endBracket 
                auxCountIdx = countIdx + 1            
            countIdx += 1
        return out



        
    def _activateA(self) -> None:
        finalOpenIdx: int = self._restText.rfind('(')
        clauseID: str = self._restText[finalOpenIdx:].split()[2]
        reducedText = self._restText[:finalOpenIdx] 
        while reducedText.count('(') > reducedText.count(')'):
            reducedText += '  )'
        assert reducedText.count('(') == reducedText.count(')')
        self._restText = reducedText
        self.ID = clauseID
        
    def _activateB(self) -> None:
        for char in self._restText:
            start: int = 0
            while not self._restText[start].isalpha():
                start += 1
            end: int = start
            while not self._restText[end].isspace():
                end += 1
        self._category = self._restText[start:end]
        
    def _activateC(self):
        tempTxt: str = self._restText 
        lastOpen: int = tempTxt.rfind('(')
        bracketStr: str = tempTxt[lastOpen:]
        if not any(x.isalpha() for x in bracketStr):
            tempTxt = tempTxt[:lastOpen]
            for i in range(bracketStr.count(')') - bracketStr.count('(')):
                tempTxt += ' ) '
        assert tempTxt.count('(') == tempTxt.count(')') 
        self._restText = tempTxt

    def _getStartIdx(self) -> tuple[str, str]:
        catIdx: int = self._restText.find(self.category)
        
        assert self._restText[catIdx-2] == '('
        assert self._restText[self._bracketPairs[catIdx-2]] == ')'
        
        return catIdx + len(self.category), self._bracketPairs[catIdx-2]

            
    # def _bracketIdxPairs(self, text : str) -> tuple:
    #     idx: int = text.find('(')
    #     left: list[int] = [idx]
    #     idx += 1 
    #     out: dict[int, int] = dict()
    #     while left:
    #         if text[idx] == '(':
    #             left.append(idx)
    #         if text[idx] == ')':
    #             l = left.pop()
    #             out[l] = idx
    #         idx += 1
    #     return out

    def __checkParsedBrackets__(self) -> None:
        for char in self.bracketPairs:
            print(self._restText[char], " - ", self._restText[self.bracketPairs[char]])



    def __str__(self) -> str:
        return f"{self._category}  {self._item} \n "
        # stack: list[TreeNode] = []
        # _ = [stack.insert(0, n)
        #      for n in self.children]
        # while stack:    
        #     node: TreeNode = stack.pop(0)
        #     _ = [stack.insert(0,n) 
        #          for n in node._children]
        #     outStr += str(node)
        # return outStr







class Tree:
    def __init__(self, clauseStr: str):
        self.root: TreeNode = RootNode(clauseStr)
        self.ID = self.root.ID

    def __str__(self) -> str:
        outStr: str =  str(self.root)
        stack: list[TreeNode] = []
        _ = [stack.insert(0, n) for n in self.root.children]

        while stack:    
            node: TreeNode = stack.pop()
            
            n: TreeNode = TreeNode()
            finalPos: int = len(stack) 
            stack.append(n)
            _ = [stack.insert(finalPos, n)
                 for n in node._children]
            stack.pop()

            outStr += str(node)
        return outStr




















