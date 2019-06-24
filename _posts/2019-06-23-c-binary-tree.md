---
layout: post
title: 用C实现一棵二叉树
date: 2019-04-08 16:08:54
categories: [读书笔记]
tags: [c,C Primer Plus]
---

用C实现一棵二叉树
<!--more-->
C Primer Plus--高级数据结构表示之二叉树


## 二叉搜索树 Binary Search Tree

二叉树是一种高级数据结构。树中的每个节点都包含一个项目和两个指向其他节点的指针。
每个节点都有两个子节点：左节点、右节点。在左节点中的项目是父节点中项目的前序向，而在右节点中的项目是父节点项目的后序向。
二叉树中每一个节点本身是其后代节点的根，此节点与其后代节点构成一个子树，子树有左右之分。
## 用C构建二叉树ADT
首先明确二叉树结构：
> 二叉树或者是一个空的节点集合（空树），或者是一个指定某个节点为根的节点集合。每个节点有两个作为其后代的树，称为左子树和右子树。
> 每个子树本身又是一个二叉树，也包含它是个空树的可能性。
> 二叉搜索树是有序的二叉树，它的每个节点包含一个项目，它的所有左子树的项目排在根项目的前面，而根项目排在所有右子树项目的前面。

而且二叉树的类型操作有：
* 树初始化为空树
* 查询树是否为空
* 查询树是否已满
* 查询树中项目个数
* 向树中添加项目
* 从树中删除项目
* 从树中搜索一个项目
* 遍历树中所有项目
* 清空树

### 树结构的定义
假设一个项目中包含一部电影的名字，上映年份，我们定义项目为`Item`：定义节点`Node`结构，包含一部电影，节点的左子节点，节点的右子节点指针；定义结构`Tree`包含根节点指针、树的项目个数。
```c
#define TITLE_MAX_CHARS 40

typedef struct movie {
    char title[TITLE_MAX_CHARS];
    int year;
} Item;

typedef struct node {
    Item movie;
    struct movie * left;
    struct movie * right;
} Node;

typedef struct tree {
    Node * root;
    int size;
} Tree;
```
定义好了数据结构，下面进行树操作的定义：
```c
//初始化树
void InitializeTree(Tree * ptoTree);

//树是空的吗？
bool TreeIsEmpty(const Tree * ptoTree);

//树满了吗？假定我们队树的最大项目树有要求
bool TreeIsFull(const Tree * ptoTree);

//查询树的项目数
bool TreeSize(const Tree * ptoTree);

//向树添加项目
bool AddMovieToTree(const Item * ptoItem,Tree * ptoTree);

//从树删除项目
bool DleteMovieFromTree(const Item * ptoItem,Tree * ptoTree);

//项目是否重复？
bool IsInTree(const Item * ptoItem, Tree * ptoTree);

//遍历树的项目
void TraverseTree(const Tree * ptoTree,void (* ptoFunc) (Item item));
```

完整程序如下：
`binarySearchTree.h`：
```c
//
// Created by bob on 2018/11/14.
//

#ifndef LEARNINGC_BINARYSEARCHTREE_H
#define LEARNINGC_BINARYSEARCHTREE_H

#include <stdbool.h>

#define MAX_ITEMS 40
#define TITLE_MAX_CHARS 40
typedef struct movie {
    char title[TITLE_MAX_CHARS];
    int year;
} Item;

typedef struct node {
    Item  movie;
    struct node * left;
    struct node * right;
} Node;

typedef struct tree {
    Node * root;
    int size;
} Tree;

typedef struct pair {
    Node * parent;
    Node * child;
} Pair;

void InitializeTree(Tree * ptoTree);

bool TreeIsEmpty(const Tree * ptoTree);

bool TreeIsFull(const Tree * ptoTree);

int TreeSize(const Tree * ptoTree);

bool AddMovieToTree(const Item * ptoItem,Tree * ptoTree);

bool DleteMovieFromTree(const Item * ptoItem,Tree * ptoTree);

bool IsInTree(const Item * ptoItem, Tree * ptoTree);

void TraverseTree(const Tree * ptoTree,void (* ptoFunc) (Item item));

void ClearTree(Tree * ptoTree);

#endif //LEARNINGC_BINARYSEARCHTREE_H

```

`binarySearchTree.c`：
```c
//
// Created by bob on 2018/11/14.
//

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "binarySearchTree.h"

static Pair SeekItem(const Item *, const Tree *);
static bool ToLeft(const Item * p1, const Item * p2);
static bool ToRight(const Item * p1, const Item * p2);
static Node * MakeNode(const Item * ptoItem);
static bool AddNodeToTree(Node * new_node, Node * root);
static bool DeleteNode(Node ** p);
static void Traverse(const Tree * ptoTree,void (*pfunc) (Item movie));
static void InOrder(const Node * parent, void (*pfunc) (Item movie));
static void DeleteAllNodes(Node * parent);
Pair SeekItem(const Item * ptoItem, const Tree * ptoTree) {

    Pair scan;
    scan.parent = NULL;
    scan.child = ptoTree->root;

    if(scan.child == NULL)
        return scan;

    while (scan.child != NULL){
        if(ToLeft(ptoItem,&(scan.child->movie))){
            scan.parent = scan.child;
            scan.child = scan.child->left;
        } else if(ToRight(ptoItem,&(scan.child->movie))){
            scan.parent = scan.child;
            scan.child = scan.child->right;
        } else{
            break;
        }
    }

    return scan;
}

bool ToLeft(const Item *p1, const Item *p2) {
    int compl;

    if((compl = strcmp(p1->title,p2->title)) < 0)
        return true;
    else if((compl = strcmp(p1->title,p2->title)) == 0 && p1->year < p2->year)
        return true;
    else
        return false;
}

bool ToRight(const Item *p1, const Item *p2) {
     int compl;

     if((compl = strcmp(p1->title,p2->title)) > 0)
         return true;
     else if((compl = strcmp(p1->title,p2->title)) == 0 && p1->year > p2->year)
         return true;
     else
         return false;
}

Node * MakeNode(const Item *ptoItem) {
    Node * new_node;
    new_node = (Node *) malloc(sizeof(Node));

    if(new_node == NULL){
        fprintf(stderr,"Can not allocate memory to create a node.\n");
        return NULL;
    }
    if(ptoItem != NULL){
        new_node->movie = * ptoItem;
        new_node->left = NULL;
        new_node->right = NULL;
    }

    return new_node;
}

bool AddNodeToTree(Node *new_node, Node * root) {
    if(ToLeft(&new_node->movie,&root->movie)){
        if(root->left == NULL)
            root->left = new_node;
        else
            AddNodeToTree(new_node,root->left);
    }else if(ToRight(&new_node->movie,&root->movie)){
        if(root->right == NULL)
            root->right = new_node;
        else
            AddNodeToTree(new_node,root->right);
    }else{
        fprintf(stderr,"Error in locating the inserting index of this node.\n");
        exit(1);
    }
    return true;
}

bool DeleteNode(Node ** p) {
    Node * p_temp;
    puts("Deleting the movie:");
    puts((*p)->movie.title);
    if((*p)->left == NULL){
        p_temp = *p;
        *p = (*p)->right;
        free(p_temp);
    } else if((*p)->right == NULL){
        p_temp = *p;
        *p = (*p)->left;
        free(p_temp);
    }else{
        for (p_temp = (*p)->left;p_temp->right != NULL;p_temp = p_temp->right)
            continue;
        p_temp->right = (*p)->right;
        p_temp = *p;
        *p = (*p)->left;
        free(p_temp);
    }
}

void Traverse(const Tree *ptoTree, void (*pfunc)(Item)) {
    if(ptoTree != NULL)
        InOrder(ptoTree->root,pfunc);
}

void InOrder(const Node *parent, void (*pfunc)(Item)) {
    if(parent != NULL){
        InOrder(parent->left,pfunc);
        (*pfunc)(parent->movie);
        InOrder(parent->right,pfunc);
    }
}

void DeleteAllNodes(Node *parent) {
    Node * ptoRight;
    if(parent != NULL){
        ptoRight = parent->right;
        DeleteAllNodes(parent->left);
        free(parent);
        DeleteAllNodes(ptoRight);
    }
}


void InitializeTree(Tree *ptoTree) {
    ptoTree -> root = NULL;
    ptoTree->size=0;
}

bool TreeIsEmpty(const Tree *ptoTree) {
    if(ptoTree->root == NULL)
        return 1;
    else
        return 0;
}

bool TreeIsFull(const Tree *ptoTree) {
    if(ptoTree->size >= MAX_ITEMS)
        return true;
    else
        return false;
}

int TreeSize(const Tree *ptoTree) {
    return ptoTree->size;
}

bool AddMovieToTree(const Item * ptoItem, Tree * ptoTree) {
    if(ptoItem == NULL | strlen(ptoItem->title) == 0 | ptoItem->year < 1800){
        fprintf(stderr,"The movie you are adding has something wrong.");
        return false;
    }
    if(TreeIsFull(ptoTree)){
        fprintf(stderr,"The tree is full. You can not add a movie to a full tree");
        return false;
    }
    if(SeekItem(ptoItem,ptoTree).child != NULL){
        fprintf(stderr,"Trying to add duplicate movie.\n");
    }

    Node * new_node;

    new_node = MakeNode(ptoItem);
//    if(new_node == NULL){
//
//    }//无需判断new_node是否为空指针，MakeNode函数里已经做过了

    ptoTree->size++;

    if(ptoTree->root == NULL)
        ptoTree->root = new_node;
    else
        AddNodeToTree(new_node,ptoTree->root);

    return true;

}

bool DleteMovieFromTree(const Item *ptoItem, Tree *ptoTree) {
    Pair scan;
    scan = SeekItem(ptoItem,ptoTree);

    if(scan.child == NULL)
        return false;

    if(scan.parent == NULL)
        DeleteNode(&ptoTree->root);
    else if(scan.parent->left == scan.child)
        //这里不能传scan.child，虽染这两个指向的是同一个node，但我们必须得传父节点持有的指针的指针
        DeleteNode(&scan.parent->left);
    else
        DeleteNode(&scan.parent->right);

    ptoTree->size--;

    return true;
}

bool IsInTree(const Item *ptoItem, Tree *ptoTree) {
    return SeekItem(ptoItem,ptoTree).child != NULL;
}

void TraverseTree(const Tree *ptoTree, void (*ptoFunc)(Item)) {
    Traverse(ptoTree,ptoFunc);
}

void ClearTree(Tree *ptoTree) {

    if(ptoTree == NULL)
        return;
    else
        DeleteAllNodes(ptoTree->root);

    ptoTree->root = NULL;
    ptoTree->size = 0;
}


```

好乱，日后再改。