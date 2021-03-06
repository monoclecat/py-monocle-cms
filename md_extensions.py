import re
from copy import deepcopy
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from markdown.util import etree

from .models import Image

import logging


class PackImagesIntoContainers(Treeprocessor):
    def run(self, root):
        new_tree = etree.Element("div")

        row_div = etree.Element("div")
        row_div.attrib["class"] = "row image_div"

        meta_tag = etree.Element("meta")

        column_div = etree.Element("div")
        column_div.attrib["class"] = "col-xs-6 col-sm-5 col-md-4 col-lg-3"

        for element in root:
            image_node = deepcopy(self.extract_images(element))
            if image_node is not None:
                # image_node[0] is an <a> tag
                tree_part = deepcopy(row_div)
                if len(list(image_node)) == 1:
                    image_node[0][0].attrib["class"] = "img-responsive single_image"
                    tree_part = deepcopy(row_div)

                    # SEO
                    tree_part.attrib["itemprop"] = "image"
                    tree_part.attrib["itemscope itemtype"] = "https://schema.org/ImageObject"
                    url_itemprop = deepcopy(meta_tag)
                    url_itemprop.attrib["itemprop"] = "url"
                    url_itemprop.attrib["content"] = image_node[0][0].attrib["src"]
                    tree_part.append(url_itemprop)

                    tree_part.append(image_node[0])
                    if "title" in image_node[0][0].attrib:
                        subtext = etree.Element("p")
                        etree.SubElement(subtext, "i")
                        subtext[0].text = image_node[0][0].attrib["title"]
                        subtext.attrib["style"] = "text-align: center;"
                        tree_part.append(subtext)
                else:
                    if len(list(image_node)) == 2:
                        col_class = ["col-xs-6 col-sm-4 col-sm-offset-4 col-md-4 col-md-offset-4 col-lg-4 col-lg-offset-4",
                                     "col-xs-6 col-sm-4 col-md-4 col-lg-4"]
                    elif len(list(image_node)) == 3:
                        col_class = ["col-xs-4 col-sm-4 col-md-4 col-lg-4",
                                     "col-xs-4 col-sm-4 col-md-4 col-lg-4", "col-xs-4 col-sm-4 col-md-4 col-lg-4"]
                    else:
                        col_class = []
                        for i in range(0, len(list(image_node))):
                            col_class.append("col-xs-6 col-sm-4 col-md-4 col-lg-4")

                    for index, image in enumerate(image_node):
                        image.attrib["class"] = "img-responsive row_image"
                        column = deepcopy(column_div)

                        column.attrib["class"] = col_class[index]
                        column.append(image)
                        tree_part.append(image)

                new_tree.append(tree_part)
            else:
                new_tree.append(element)
        return new_tree

    def extract_images(self, node):
        if node.tag == 'p':
            if len(list(node)) != 0:
                extracted = []
                for child in node:
                    if len(list(child)) == 1 and child.tag == 'a' and child[0].tag == 'img':
                        extracted.append(child)
                    else:
                        return None
                return extracted
        return None


class PackImgBarebones(Treeprocessor):
    def run(self, root):
        new_tree = etree.Element("div")

        row_div = etree.Element("div")
        row_div.attrib["class"] = "row"

        column_div = etree.Element("div")
        column_div.attrib["class"] = "col-xs-12"

        for element in root:
            image_node = deepcopy(self.extract_images(element))
            if image_node is not None:
                # image_node[0] is an <a> tag
                tree_part = deepcopy(row_div)
                if len(list(image_node)) == 1:
                    image_node[0][0].attrib["class"] = "img-responsive single_image"
                    image_node[0][0].attrib["style"] = "padding:7px 7px; width: 100%;"
                    tree_part = deepcopy(row_div)
                    # By appending image_node[0][0] instead of image_node[0] as in the original function,
                    # we remove the link to the original image, which is our wish for the index page
                    tree_part.append(image_node[0][0])
                else:
                    logging.warning("PackImgBarebones got a 2 element image node!")

                new_tree.append(tree_part)
            else:
                new_tree.append(element)
        return new_tree

    def extract_images(self, node):
        if node.tag == 'p':
            if len(list(node)) != 0:
                extracted = []
                for child in node:
                    if len(list(child)) == 1 and child.tag == 'a' and child[0].tag == 'img':
                        extracted.append(child)
                    else:
                        return None
                return extracted
        return None


class InsertImgLinks(Preprocessor):
    def run(self, lines):
        pattern = re.compile(r' *\!\[ *(?P<alt_text>[^]]*) *\] *\( *(?P<pk>\d+) +(?P<size>(small|medium|large)) +"(?P<title>[^]"]*)" *\) *')
        new_lines = []
        for line in lines:
            m = pattern.match(line)
            if m:
                try:
                    img_link = Image.objects.get(pk=m.group('pk')).file.url
                    if m.group('size') == 'small':
                        img = Image.objects.get(pk=m.group('pk')).file.small.url
                    elif m.group('size') == 'medium':
                        img = Image.objects.get(pk=m.group('pk')).file.medium.url
                    else:
                        img = Image.objects.get(pk=m.group('pk')).file.large.url
                    new_lines.append(
                        "[![" + m.group('alt_text') + "](" + img + " \"" + m.group('title') + "\")]("+img_link+")")
                except Image.DoesNotExist:
                    pass
            else:
                new_lines.append(line)
        return new_lines


class RemoveImages(Preprocessor):
    def run(self, lines):
        pattern = re.compile(r' *\!\[ *(?P<alt_text>[^]]*) *\] *\( *(?P<pk>\d+) +(?P<size>(small|medium|large)) +"(?P<title>[^]"]*)" *\) *')
        new_lines = []
        for line in lines:
            m = pattern.match(line)
            if m:
                pass
            else:
                new_lines.append(line)
        return new_lines


class FirstImage(Preprocessor):
    def run(self, lines):
        pattern = re.compile(r' *\!\[ *(?P<alt_text>[^]]*) *\] *\( *(?P<pk>\d+) +(?P<size>(small|medium|large)) +"(?P<title>[^]"]*)" *\) *')
        new_lines = []
        for line in lines:
            m = pattern.match(line)
            if m:
                try:
                    img_link = Image.objects.get(pk=m.group('pk')).file.url
                    img = Image.objects.get(pk=m.group('pk')).file.large.url
                    new_lines.append(
                        "[![" + m.group('alt_text') + "](" + img + " \"\")]("+img_link+")")
                    break
                except Image.DoesNotExist:
                    pass
            else:
                pass
        return new_lines


class PageBuildingExtensions(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors['insert_img_links'] = InsertImgLinks(md)
        md.treeprocessors['pack_img_into_cont'] = PackImagesIntoContainers(md)


class NoImgExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors['insert_img_links'] = RemoveImages(md)


class FirstImgExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors['insert_img_links'] = FirstImage(md)
        md.treeprocessors['pack_img_into_cont'] = PackImgBarebones(md)
