#NOSTILL

## About

**Nostill** is a website for curated content in the field of digital animation that is suitable for mainstream consumption and appreciation. Some types of content that is gathered by **Nostill** are *3d animation*, *visual effects*, *motion graphics*, etc...

## Why Nostill?

**Vimeo** is an excellent source for digital animation. Even though the content quality there is pretty high and it supports creation of and subscription to custom playlists, etc... it still is hard to use as a resource for casual consumption of high quality digital content. It is rather popular which makes it cluttered and hard to navigate through all the content. These reasons validate the creation of a *wrapper* web app that would gather curated content from vimeo (and other resources as well) by industry professional and present it in a more refined way.

## Really, Why?

I wanted to learn web app development using Python and Django, and starting out with a straightforward project like **nostill ** was a rather easy way to get started.

## Workflow

- have a user that you are **liking** videos with in a video website. (like **vimeo**)
- fetch the data for the liked videos from through their API
  - might need to refine the captured data; better descriptions, automated tagging, etc
- verify and refine the content of the initial database you have created.
- append this to the database for your web app.
- present the items in this database in a pleasant way for general user consumption.

## Roadmap

- Enables categorization of the content it presents for filtering by the user (like: see only animation videos, etc..)
- Has a rating system based on the vimeo data.
  - This means, the rating of the linked vimeo video should be fetched everytime the video is     loaded.
- Should present some awesome recent videos for easy access.